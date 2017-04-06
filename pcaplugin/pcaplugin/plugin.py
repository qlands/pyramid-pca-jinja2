import pcaexample.plugins as plugins
import pcaexample.plugins.utilities as u
from .views import my_view

class PCAExamplePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IRoutes)
    plugins.implements(plugins.IConfig)

    def before_mapping(self, config):
        return []

    def after_mapping(self, config):
        custom_map = []
        custom_map.append({'name': 'json', 'path': '/json', 'view': my_view, 'renderer': 'json'})
        return custom_map

    def update_config(self, config):
        u.addTemplatesDirectory(config,'templates')
        u.addStaticView(config,'pstatic','pstatic')
