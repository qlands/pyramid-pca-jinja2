import os

import pcaexample.plugins as p
import pcaexample.resources as r
from .jinja_extensions import (
    initialize,
    ExtendThis,
    JSResourceExtension,
    CSSResourceExtension,
)
from pcaexample.routes import load_routes
import pcaexample.plugins.helpers as helpers


def __url_for_static(request, static_file, library="static"):
    """
    This function return the address of a static URL. It substitutes request.static_url because static_url does not
    work for plugins when using a full path to the static directory
    :param request: Current request object
    :param static_file: Static file being requested
    :param library: Library where the static file is located
    :return: URL to the static resource
    """
    return request.application_url + "/" + library + "/" + static_file


def __helper(request):
    h = helpers.helper_functions
    return h


class RequestResources(object):
    """
    This class handles the injection of resources in templates
    """

    def __init__(self, request):
        self.request = request
        self.current_resources = []

    def add_resource(self, library_name, resource_id, resource_type):
        self.current_resources.append(
            {
                "libraryName": library_name,
                "resourceID": resource_id,
                "resourceType": resource_type,
            }
        )

    def resource_in_request(self, library_name, resource_id, resource_type):
        for resource in self.current_resources:
            if (
                resource["libraryName"] == library_name
                and resource["resourceID"] == resource_id
                and resource["resourceType"] == resource_type
            ):
                return True
        return False


def load_environment(settings, config, apppath):
    config.registry.settings["jinja2.extensions"] = [
        ExtendThis,
        JSResourceExtension,
        CSSResourceExtension,
    ]

    config.include("pyramid_jinja2")
    # Add url_for_static to the request so plugins can use static resources
    config.add_request_method(__url_for_static, "url_for_static")
    # Add active resources to the request. This control the injection of resources into a request
    config.add_request_method(RequestResources, "activeResources", reify=True)

    # Add a series of helper functions to the request like pluralize
    helpers.load_plugin_helpers()
    config.add_request_method(__helper, "h", reify=True)

    # Add core fanstatic library
    r.add_library("coreresources", os.path.join(apppath, "js_and_css"), config)

    # Add core CSS and JS
    r.add_css_resource("coreresources", "bootstrapcss", "bootstrap.min.css")
    r.add_css_resource("coreresources", "font-5", "fontawesome/css/all.css")
    r.add_css_resource("coreresources", "font-awesome", "fontawesome/css/v4-shims.css")
    r.add_css_resource("coreresources", "theme", "theme.css")
    r.add_js_resource("coreresources", "jquery", "jquery.min.js")
    r.add_js_resource("coreresources", "bootstrap", "bootstrap.min.js")

    # Add the static view
    static_path = os.path.join(apppath, "static")
    config.add_static_view("static", static_path, cache_max_age=3600)

    templatesPathArray = []
    templatesPath = os.path.join(apppath, "templates")
    templatesPathArray.append(templatesPath)

    config.add_settings(templatesPaths=templatesPathArray)

    config.add_jinja2_search_path(templatesPath)

    # Load all connected plugins
    p.load_all(settings)

    # Load any change in the configuration done by connected plugins
    for plugin in p.PluginImplementations(p.IConfig):
        plugin.update_config(config)

    # Call any connected plugins to add their libraries
    for plugin in p.PluginImplementations(p.IResource):
        pluginLibraries = plugin.add_libraries(config)
        for library in pluginLibraries:
            r.add_library(library["name"], library["path"], config)

    # Call any connected plugins to add their CSS Resources
    for plugin in p.PluginImplementations(p.IResource):
        cssResources = plugin.add_css_resources(config)
        for resource in cssResources:
            r.add_css_resource(
                resource["libraryname"],
                resource["id"],
                resource["file"],
                resource["depends"],
            )

    # Call any connected plugins to add their JS Resources
    for plugin in p.PluginImplementations(p.IResource):
        jsResources = plugin.add_js_resources(config)
        for resource in jsResources:
            r.add_js_resource(
                resource["libraryname"],
                resource["id"],
                resource["file"],
                resource["depends"],
            )

    # jinjaEnv is used by the jinja2 extensions so we get it from the config
    config.get_jinja2_environment()

    # setup the jinjaEnv template's paths for the extensions
    initialize(config.registry.settings["templatesPaths"])

    # Finally we load the routes
    load_routes(config)
