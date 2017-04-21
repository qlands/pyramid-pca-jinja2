# An extendable Pyramid application using PCA and Jinja2 plugins

[Pyramid]( https://trypyramid.com/) is a great framework for developing web applications that also supports the development of ["Extensible" and "Pluggable"]( http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/extending.html) software based on certain rules. However, there is no much documentation on how to create such type of applications.

[CKAN]( https://ckan.org/) is an excellent example of a Web application that can be extended or customized using plugins. It relies on [PyUtilib Component Architecture]( https://pypi.python.org/pypi/PyUtilib) to declare a series of interfaces and extension points that then are used by plugins to hook in. It also implements a series of [Jinja2]( http://jinja.pocoo.org/) extension (notably CKAN_EXTENDS) that allows easily template inheritance between CKAN and connected plugins. For resources like CSS and JS CKAN uses [Fanstatic](http://www.fanstatic.org/en/1.0a5/) and also allows plugins to define new resources.

CKAN however is developed using [Pylons](http://pylonsproject.org/about-pylons-framework.html) which is now superseded by Pyramid and coupled to its complexity makes it difficult to grasp how to apply such extensibility to Pyramid web applications.

This example applies a modified version of CKAN extensible system to a simple Pyramid application that can be used as a starter to develop more complex extendable web applications. The example allows plugins to extend the host by:
 - Adding new routes
 - Adding and overwriting templates
 - Adding new static resources
 - Adding new Fanstatic resources
 - Easy Jinja2 template inheritance and resource injection


The example (pcaexample) is based on a “pyramid-cookiecutter-alchemy” [Cookiecutter](https://github.com/audreyr/cookiecutter) while the plugin is based on a “pyramid-cookiecutter-starter”. It uses Pyramid 1.8.3 with PyUtilib 5.4.1.

Please note that the example implements Pyramid "Extensible" and "Pluggable" capabilities in a way that I feel it would satisfy most needs but it might not be the best or the most logical way of doing it. **Comments and suggestions are welcomed.**

## Installation and testing
To build and run the example host application (pcaexample) on Linux do:

    $ git clone https://github.com/qlands/pyramid-pca-jinja2.git
    $ virtualenv pcaexample_env
    $ . ./pcaexample_env/bin/activate
    $ cd pyramid-pca-jinja2
    $ cd pcaexample
    $ python setup.py install
    $ initialize_pcaexample_db ./development.ini
    $ pserve ./development.ini

To build the a example of the plugin (pcaplugin) on Linux do:

    $ cd pyramid-pca-jinja2
    $ cd pcaplugin
    $ python setup.py develop
    $ cd ..
    $ cd pcaexample


Edit the configuration of the host application (development.ini) to load the plugin by **uncommenting line 20**.
> #pcaexample.plugins = examplePlugin [**change to**]  pcaexample.plugins = examplePlugin

Then do:

    $ pserve ./development.init

## Screenshot

![Image](/screenshot.png?raw=true "Example home screen with and without plugin")


## Author
Carlos Quiros (cquiros_at_qlands.com / c.f.quiros_at_cgiar.org)