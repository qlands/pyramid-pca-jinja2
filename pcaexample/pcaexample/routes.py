'''

These functions setup the routes for the host application and any plugins connected to it

'''

from pcaexample.views.default import my_view
from pcaexample.views.notfound import notfound_view
import pcaexample.plugins as p

route_list = []

#This function append or overrides the routes to the main list
def appendToRoutes(routeList):
    for new_route in routeList:
        found = False
        pos = 0
        for curr_route in route_list:
            if curr_route['path'] == new_route['path']:
                found = True
        pos += 1
        if not found:
            route_list.append(new_route)
        else:
            route_list[pos]['name'] = new_route['name']
            route_list[pos]['view'] = new_route['view']
            route_list[pos]['renderer'] = new_route['renderer']


def loadRoutes(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

    # Custom mapping can happen here BEFORE the host maps
    for plugin in p.PluginImplementations(p.IRoutes):
        routes = plugin.before_mapping(config)
        appendToRoutes(routes)

    # These are the routes of the host application
    routes = []
    routes.append({'name':'home','path':'/','view':my_view,'renderer':'mytemplate.jinja2'})
    appendToRoutes(routes)

    config.add_notfound_view(notfound_view,renderer='404.jinja2')

    # Custom mapping can happen here AFTER the host maps
    for plugin in p.PluginImplementations(p.IRoutes):
        routes = plugin.after_mapping(config)
        appendToRoutes(routes)

    # Now add the routes and views to the config
    for curr_route in route_list:
        config.add_route(curr_route['name'], curr_route['path'])
        config.add_view(curr_route['view'], route_name=curr_route['name'], renderer=curr_route['renderer'])
