"""

These functions setup the routes for the host application and any plugins connected to it

"""
from .plugins.utilities import add_route
from pcaexample.views.default import my_view
from pcaexample.views.notfound import notfound_view
from pcaexample.views.error import error_view
import pcaexample.plugins as p

route_list = []


def append_to_routes(route_array):
    """
    #This function append or overrides the routes to the main list
    :param route_array: Array of routes
    """
    for new_route in route_array:
        found = False
        pos = 0
        for curr_route in route_list:
            if curr_route["path"] == new_route["path"]:
                found = True
        pos += 1
        if not found:
            route_list.append(new_route)
        else:
            route_list[pos]["name"] = new_route["name"]
            route_list[pos]["view"] = new_route["view"]
            route_list[pos]["renderer"] = new_route["renderer"]


def load_routes(config):
    """
    Call connected to plugins to add any routes before FormShare
    :param config: Pyramid config
    """
    routes = []

    for plugin in p.PluginImplementations(p.IRoutes):
        routes = plugin.before_mapping(config)
        append_to_routes(routes)

    # FormShare routes
    routes.append(add_route("home", "/", my_view, "mytemplate.jinja2"))

    config.add_notfound_view(notfound_view, renderer="404.jinja2")
    config.add_view(error_view, context=Exception, renderer="500.jinja2")

    append_to_routes(routes)

    # Call connected plugins to add any routes after FormShare
    for plugin in p.PluginImplementations(p.IRoutes):
        routes = plugin.after_mapping(config)
        append_to_routes(routes)

    # Now add the routes and views to the Pyramid config
    for curr_route in route_list:
        print("Addin route")
        config.add_route(curr_route["name"], curr_route["path"])
        config.add_view(
            curr_route["view"],
            route_name=curr_route["name"],
            renderer=curr_route["renderer"],
        )

    print("Routes loaded")