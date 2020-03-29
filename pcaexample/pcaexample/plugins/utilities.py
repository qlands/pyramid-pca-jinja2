"""
These series of functions help plugin developers
to manipulate the host behaviour without the trouble if dealing with it
"""

import inspect
import os

__all__ = [
    "add_templates_directory",
    "add_static_view",
    "add_js_resource",
    "add_css_resource",
    "add_library",
    "add_route",
]


def __return_current_path():
    """
    This code is based on CKAN
    :Copyright (C) 2007 Open Knowledge Foundation
    :license: AGPL V3, see LICENSE for more details.
    :return:
    """
    frame, filename, line_number, function_name, lines, index = inspect.getouterframes(
        inspect.currentframe()
    )[2]
    return os.path.dirname(filename)


def add_templates_directory(config, relative_path, prepend=True):
    caller_path = __return_current_path()
    templates_path = os.path.join(caller_path, relative_path)
    if os.path.exists(templates_path):
        config.add_jinja2_search_path(searchpath=templates_path, prepend=prepend)
        if prepend:
            config.registry.settings["templatesPaths"].insert(0, templates_path)
        else:
            config.registry.settings["templatesPaths"].append(templates_path)
    else:
        raise Exception("Templates path {} does not exists".format(relative_path))


def add_static_view(config, view_name, relative_path, cache_max_age=3600):
    caller_path = __return_current_path()
    static_path = os.path.join(caller_path, relative_path)
    if os.path.exists(static_path):
        introspector = config.introspector
        if introspector.get("static views", view_name, None) is None:
            config.add_static_view(view_name, static_path, cache_max_age=cache_max_age)
    else:
        raise Exception("Static path {} does not exists".format(relative_path))


def add_js_resource(library_name, resource_id, resource_file, depends="CHAIN"):
    return {
        "libraryname": library_name,
        "id": resource_id,
        "file": resource_file,
        "depends": depends,
    }


def add_css_resource(library_name, resource_id, resource_file, depends="CHAIN"):
    return {
        "libraryname": library_name,
        "id": resource_id,
        "file": resource_file,
        "depends": depends,
    }


def add_library(name, path):
    caller_path = __return_current_path()
    library_path = os.path.join(caller_path, path)
    if os.path.exists(library_path):
        return {"name": name, "path": library_path}
    else:
        raise Exception("Library path {} does not exists".format(path))


def add_route(name, path, view, renderer):
    return {"name": name, "path": path, "view": view, "renderer": renderer}
