'''
This files configure host application

This code is based on CKAN 
:Copyright (C) 2007 Open Knowledge Foundation
:license: AGPL V3, see LICENSE for more details.

'''

import os

import pcaexample.plugins as p
import pcaexample.resources as r
from jinja_extensions import initialize, SnippetExtension, extendThis, ResourceExtension
from pcaexample.routes import loadRoutes


# This function return the address of a static URL.
# It substitutes request.static_url because
# static_url does not work for plugins when using
# a full path to the static directory
def __url_for_static(request,static_file):
    return request.host_url + '/' + static_file

def load_environment(settings,config,apppath):

    class resourceFoundException(Exception):
        def __init__(self, msg):
            self.msg = msg

    config.registry.settings['jinja2.extensions'] = [SnippetExtension,extendThis,ResourceExtension]

    config.include('pyramid_jinja2')
    config.include('pyramid_fanstatic')
    config.add_request_method(__url_for_static, 'url_for_static')

    # Add core fanstatic library
    r.addLibrary('coreresources',os.path.join(apppath, 'fanstatic'))

    # Add core CSS and JS
    r.addCSSResource('coreresources','bootstrapcss','bootstrap.min.css')
    r.addCSSResource('coreresources', 'theme', 'theme.css')
    r.addJSResource('coreresources','jquery','jquery.min.js')
    r.addJSResource('coreresources', 'bootstrap', 'bootstrap.min.js')


    templatesPathArray =[]
    templatesPath = os.path.join(apppath, 'templates')
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
            r.addLibrary(library["name"], library["path"])

    # Call any connected plugins to add their CSS Resources
    for plugin in p.PluginImplementations(p.IResource):
        cssResources = plugin.add_CSSResources(config, r.getCSSResourceList())
        for resource in cssResources:
            if resource["depends"] != "CHAIN" and resource["id"] != "CHAIN":
                r.addCSSResource(resource["libraryname"], resource["id"], resource["file"], resource["depends"])
            else:
                if resource["depends"] != "CHAIN":
                    raise resourceFoundException("Plugin resources cannot be chained")
                else:
                    raise resourceFoundException("Plugin resources cannot have CHAIN as ID")

    # Call any connected plugins to add their JS Resources
    for plugin in p.PluginImplementations(p.IResource):
        jsResources = plugin.add_JSResources(config, r.getJSResourceList())
        for resource in jsResources:
            if resource["depends"] != "CHAIN":
                r.addJSResource(resource["libraryname"], resource["id"], resource["file"], resource["depends"])
            else:
                if resource["depends"] != "CHAIN":
                    raise resourceFoundException("Plugin resources cannot be chained")
                else:
                    raise resourceFoundException('Plugin resources cannot have "CHAIN" as ID')


    # jinjaEnv is used by the jinja2 extensions so we get it from the config
    jinjaEnv = config.get_jinja2_environment()

    # setup the jinjaEnv template's paths for the extensions
    initialize(config.registry.settings['templatesPaths'])

    # Finally we load the routes
    loadRoutes(config)


