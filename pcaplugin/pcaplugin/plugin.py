import pcaexample.plugins as plugins
import pcaexample.plugins.utilities as u
from .views import my_view

class PCAExamplePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IRoutes)
    plugins.implements(plugins.IConfig)
    plugins.implements(plugins.IResource)

    def before_mapping(self, config):
        #We don't add any routes before the host application
        return []

    def after_mapping(self, config):
        #We add here a new route /json that returns a JSON
        custom_map = []
        custom_map.append(u.addRoute('json','/json',my_view,'json'))
        return custom_map

    def update_config(self, config):
        #We add here the templates and static directories of the plugin to the config
        u.addTemplatesDirectory(config,'templates')
        u.addStaticView(config,'pstatic','static')

    def add_libraries(self,config):
        #We add here our new library using the fanstatic directory of the plugin
        libraries = []
        libraries.append(u.addLibrary('plibrary','fanstatic'))
        return libraries

    def add_JSResources(self, config):
        # We add here two new JavaScripts: leaflet and mymap.js so we can required then later on in mytemplate.jinja2
        # The JS of leaflet required bootstrap so it will be included after the JS of bootstrap
        # My map requires leaflet so if we need mymap it will include the JS of leaflet
        myJS = []
        myJS.append(u.addJSResource('plibrary','leaflet','leaflet/leaflet.js'))
        myJS.append(u.addJSResource('plibrary', 'mymap', 'mymap.js'))
        return myJS

    def add_CSSResources(self, config):
        # We add here the new css for leaflet we can required it later on in mytemplate.jinja2
        myCSS = []
        myCSS.append(u.addCSSResource('plibrary', 'leaflet', 'leaflet/leaflet.css'))
        return myCSS


