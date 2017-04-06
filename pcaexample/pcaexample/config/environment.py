'''
This files configure host application

This code is based on CKAN 
:Copyright (C) 2007 Open Knowledge Foundation
:license: AGPL V3, see LICENSE for more details.

'''

import pcaexample.plugins as p
from pcaexample.routes import loadRoutes
import os
from jinja_extensions import initialize, jinjaEnv, SnippetExtension, extendThis

# This function return the address of a static URL.
# It substitutes request.static_url because
# static_url does not work for plugins when using
# a full path to the static directory
def __url_for_static(request,static_file):
    return request.host_url + '/' + static_file

def load_environment(settings,config,apppath):

    config.registry.settings['jinja2.extensions'] = [SnippetExtension,extendThis]

    config.include('pyramid_jinja2')
    config.add_request_method(__url_for_static, 'url_for_static')

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

    # jinjaEnv is used by the jinja2 extensions so we get it from the config
    jinjaEnv = config.get_jinja2_environment()

    # setup the jinjaEnv template's paths for the extensions
    initialize(config.registry.settings['templatesPaths'])

    # Finally we load the routes
    loadRoutes(config)


