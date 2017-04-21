from fanstatic import Library, Resource, get_library_registry
from exceptions import Exception
import os

__all__ = [
    'addLibrary', 'addJSResource',
    'addCSSResource', 'getJSResource', 'getCSSResource',
    'getLibraryList', 'getCSSResourceList', 'getJSResourceList'
]

_LIBRARIES = []
_CSSRESOURCES = []
_JSRESOURCES = []

def library_found(name):
    for library in _LIBRARIES:
        if library["name"] == name:
            return True
    return False

def library_index(name):
    for pos in range(0,len(_LIBRARIES)):
        if _LIBRARIES[pos]["name"] == name:
            return pos
    return -1

def library_path_exits(path):
    return os.path.exists(path)

def library_path_found(path):
    for library in _LIBRARIES:
        if os.path.normpath(library["path"]) == os.path.normpath(path):
            return True
    return False


class libraryFoundException(Exception):
    def __init__(self, msg):
        self.msg = msg

def addLibrary(name,path):

    class libraryPathException(Exception):
        def __init__(self, msg):
            self.msg = msg

    if not library_found(name):
        if library_path_exits(path):
            if not library_path_found(path):
                _LIBRARIES.append({'name': name,'path': path,'library': Library(name, path)})
                registry = get_library_registry()
                registry.add(_LIBRARIES[len(_LIBRARIES)-1]["library"])
            else:
                raise libraryPathException("Path %s already in use" % path)
        else:
            raise libraryPathException("Path %s not found" % path)
    else:
        raise libraryFoundException("Library name %s is already in use" % name)

def resourceExists(resourceID,resourceType='JS'):
    if resourceType == 'JS':
        for resource in _JSRESOURCES:
            if resource["resourceID"] == resourceID:
                return True
    if resourceType == 'CSS':
        for resource in _CSSRESOURCES:
            if resource["resourceID"] == resourceID:
                return True
    return False

def resourceIndex(resourceID,resourceType='JS'):
    if resourceType == 'JS':
        for index in range(0,len(_JSRESOURCES)) :
            if _JSRESOURCES[index]["resourceID"] == resourceID:
                return index
    if resourceType == 'CSS':
        for index in range(0, len(_CSSRESOURCES)):
            if _CSSRESOURCES[index]["resourceID"] == resourceID:
                return index
    return -1


class resourceFoundException(Exception):
    def __init__(self, msg):
        self.msg = msg

def addResource(libraryName,resourceID,resourceFile,resourceType='JS',depends='CHAIN'):
    index = library_index(libraryName)
    if index >= 0:
        libraryPath = _LIBRARIES[index]["path"]
        pathToResource = os.path.join(libraryPath, resourceFile)
        if os.path.exists(pathToResource):
            if not resourceExists(resourceID,resourceType):
                if resourceType == 'JS':
                    if len(_JSRESOURCES) == 0:
                        _JSRESOURCES.append({'resourceID':resourceID,'file':resourceFile,'resource':Resource(_LIBRARIES[index]["library"],resourceFile,bottom=True),'library':libraryName,'depends':None})
                    else:
                        if depends == 'CHAIN':
                            _JSRESOURCES.append({'resourceID': resourceID,'file':resourceFile,
                                                 'resource': Resource(_LIBRARIES[index]["library"], resourceFile,
                                                                      depends=[_JSRESOURCES[len(_JSRESOURCES) - 1][
                                                                          "resource"]], bottom=True),'library':libraryName,'depends':_JSRESOURCES[len(_JSRESOURCES) - 1][
                                                                          "resourceID"]})
                        else:
                            if depends is None:
                                _JSRESOURCES.append({'resourceID': resourceID,'file':resourceFile,
                                                 'resource': Resource(_LIBRARIES[index]["library"], resourceFile, bottom=True),'library':libraryName,'depends':None})
                            else:
                                depIndex = resourceIndex(depends)
                                if depIndex >= 0:
                                    _JSRESOURCES.append({'resourceID': resourceID,'file':resourceFile,
                                                         'resource': Resource(_LIBRARIES[index]["library"], resourceFile,
                                                                              depends=[_JSRESOURCES[depIndex]["resource"]], bottom=True),'library':libraryName,'depends':depends})
                                else:
                                    raise resourceFoundException("Dependency resource %s does not exists" % depends)
                if resourceType == 'CSS':
                    if len(_CSSRESOURCES) == 0:
                        _CSSRESOURCES.append({'resourceID':resourceID,'file':resourceFile,'resource':Resource(_LIBRARIES[index]["library"],resourceFile),'library':libraryName,'depends':None})
                    else:
                        if depends == 'CHAIN':
                            _CSSRESOURCES.append({'resourceID': resourceID,'file':resourceFile,
                                                  'resource': Resource(_LIBRARIES[index]["library"], resourceFile,
                                                                       depends=[_CSSRESOURCES[len(_CSSRESOURCES) - 1][
                                                                           "resource"]]),'library':libraryName,'depends':_CSSRESOURCES[len(_CSSRESOURCES) - 1][
                                                                           "resourceID"]})
                        else:
                            if depends is None:
                                _CSSRESOURCES.append({'resourceID': resourceID,'file':resourceFile,
                                                      'resource': Resource(_LIBRARIES[index]["library"], resourceFile),'library':libraryName,'depends':None})
                            else:
                                depIndex = resourceIndex(depends,'CSS')
                                if depIndex >= 0:
                                    _CSSRESOURCES.append({'resourceID': resourceID,'file':resourceFile,
                                                          'resource': Resource(_LIBRARIES[index]["library"],
                                                                               resourceFile,
                                                                               depends=[
                                                                               _CSSRESOURCES[depIndex]["resource"]]),'library':libraryName,'depends':depends})
                                else:
                                    raise resourceFoundException("Dependency resource %s does not exists" % depends)
            else:
                raise resourceFoundException("Resource id %s already in list" % resourceID)
        else:
            raise resourceFoundException("Resource file %s does not exists" % resourceFile)
    else:
        raise libraryFoundException("Library name %s does not exists" % libraryName)

def addJSResource(libraryName,resourceID,resourceFile,depends='CHAIN'):
    addResource(libraryName,resourceID,resourceFile,'JS',depends)

def addCSSResource(libraryName,resourceID,resourceFile,depends='CHAIN'):
    addResource(libraryName,resourceID,resourceFile,'CSS',depends)

def getJSResource(resourceID):
    index = resourceIndex(resourceID)
    if index >= 0:
        return _JSRESOURCES[index]["resource"]
    else:
        raise resourceFoundException("Resource %s does not exists" % resourceID)

def getCSSResource(resourceID):
    index = resourceIndex(resourceID,'CSS')
    if index >= 0:
        return _CSSRESOURCES[index]["resource"]
    else:
        raise resourceFoundException("Resource %s does not exists" % resourceID)

def getLibraryList():
    result = []
    for library in _LIBRARIES:
        result.append({'name': library["name"],'path': library["path"]})
    return result

def getCSSResourceList():
    result = []
    for resource in _CSSRESOURCES:
        result.append({'resourceID':resource["resourceID"],'file':resource["file"],'library':resource["library"],'depends':resource["depends"]})
    return result

def getJSResourceList():
    result = []
    for resource in _JSRESOURCES:
        result.append({'resourceID':resource["resourceID"],'file':resource["file"],'library':resource["library"],'depends':resource["depends"]})
    return result

