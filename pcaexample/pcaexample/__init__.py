from .config.environment import load_environment
from pyramid.config import Configurator
import os

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    config = Configurator(settings=settings)
    apppath = os.path.dirname(os.path.abspath(__file__))
    # Load and configure the host application
    load_environment(settings,config,apppath)

    config.include('.models')
    return config.make_wsgi_app()
