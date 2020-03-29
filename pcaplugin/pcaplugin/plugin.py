import pcaexample.plugins as plugins
import pcaexample.plugins.utilities as u
from .views import my_view


class PCAExamplePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IRoutes)
    plugins.implements(plugins.IConfig)
    plugins.implements(plugins.IResource)

    # Implement IRoutes
    def before_mapping(self, config):
        # We don't add any routes before the host application
        return []

    def after_mapping(self, config):
        # We add here a new route /json that returns a JSON
        custom_map = []
        custom_map.append(u.add_route("json", "/json", my_view, "json"))
        return custom_map

    # Implements IConfig
    def update_config(self, config):
        # We add here the templates and static directories of the plugin to the config
        u.add_templates_directory(config, "templates")
        u.add_static_view(config, "pstatic", "static")

    # Implements IResource
    def add_libraries(self, config):
        # We add here our new library using the fanstatic directory of the plugin
        libraries = []
        libraries.append(u.add_library("plibrary", "js_and_css"))
        return libraries

    def add_js_resources(self, config):
        # We add here two new JavaScripts: leaflet and mymap.js so we can required then later on in mytemplate.jinja2
        # The JS of leaflet required bootstrap so it will be included after the JS of bootstrap
        # My map requires leaflet so if we need mymap it will include the JS of leaflet
        myJS = []
        myJS.append(u.add_js_resource("plibrary", "leaflet", "leaflet/leaflet.js"))
        myJS.append(u.add_js_resource("plibrary", "mymap", "mymap.js"))
        return myJS

    def add_css_resources(self, config):
        # We add here the new css for leaflet we can required it later on in mytemplate.jinja2
        myCSS = []
        myCSS.append(u.add_css_resource("plibrary", "leaflet", "leaflet/leaflet.css"))
        return myCSS
