'''
These series of functions help plugin developers 
to manipulate the host behaviour without the trouble if dealing with it

This code is based on CKAN 
:Copyright (C) 2007 Open Knowledge Foundation
:license: AGPL V3, see LICENSE for more details.

'''

import inspect
import os
import pcaexample.resources as r
from exceptions import Exception

class resourceFoundException(Exception):
    def __init__(self, msg):
        self.msg = msg

class invalidPathException(Exception):
    def __init__(self, msg):
        self.msg = msg

def __returnCurrentPath():
    frame, filename, line_number, function_name, lines, index = \
        inspect.getouterframes(inspect.currentframe())[2]
    return os.path.dirname(filename)

def addTemplatesDirectory(config,relative_path,prepend=True):
    callerPath = __returnCurrentPath()
    templates_path = os.path.join(callerPath, relative_path)
    if os.path.exists(templates_path):
        config.add_jinja2_search_path(searchpath=templates_path,prepend=prepend)
        if prepend == True:
            config.registry.settings['templatesPaths'].insert(0,templates_path)
        else:
            config.registry.settings['templatesPaths'].append(templates_path)
    else:
        raise invalidPathException("Templates path %s does not exists" % relative_path)

def addStaticView(config,viewName,relative_path,cache_max_age=3600):
    callerPath = __returnCurrentPath()
    static_path = os.path.join(callerPath, relative_path)
    if os.path.exists(static_path):
        introspector = config.introspector
        if introspector.get('static views', viewName,None) is None:
            config.add_static_view(viewName, static_path, cache_max_age=cache_max_age)
    else:
        raise invalidPathException("Static path %s does not exists" % relative_path)

def addJSResource(libraryName,resourceID,resourceFile,depends):
    return {'libraryname':libraryName,'id':resourceID,'file':resourceFile,'depends':depends}

def addCSSResource(libraryName,resourceID,resourceFile,depends):
    return {'libraryname': libraryName, 'id': resourceID, 'file': resourceFile, 'depends': depends}

def addLibrary(name,path):
    callerPath = __returnCurrentPath()
    library_path = os.path.join(callerPath, path)
    if os.path.exists(library_path):
        return {'name':name,'path':library_path}
    else:
        raise invalidPathException("Library path %s does not exists" % path)

def addRoute(name,path,view,renderer):
    return {'name': name, 'path': path, 'view': view, 'renderer': renderer}

def getJSResource(resourceID):
    return r.getJSResource(resourceID)

def getCSSResource(resourceID):
    return r.getCSSResource(resourceID)
