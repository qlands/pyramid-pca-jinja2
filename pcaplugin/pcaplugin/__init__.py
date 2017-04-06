#from pyramid.config import Configurator


# def main(global_config, **settings):
#     """ This function returns a Pyramid WSGI application.
#     """
#     config = Configurator(settings=settings)
#     config.include('pyramid_jinja2')
#     config.add_static_view('pstatic', 'pstatic', cache_max_age=3600)
#     config.add_route('home', '/')
#     config.scan()
#     return config.make_wsgi_app()

try:
    import pkg_resources
    pkg_resources.declare_namespace(__name__)
except ImportError:
    import pkgutil
    __path__ = pkgutil.extend_path(__path__, __name__)
