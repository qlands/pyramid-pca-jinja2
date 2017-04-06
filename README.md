# An extendable Pyramid application using PCA and Jinja2 plugins

[Pyramid]( https://trypyramid.com/) is a great framework for developing web applications that also support the development of ["Extensible" and "Pluggable"]( http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/extending.html) software based on certain rules. However, there is no much documentation on how to create such type of applications.

[CKAN]( https://ckan.org/) is an excellent example of a Web application that can be extended or customized using plugins. It relies on [PyUtilib Component Architecture]( https://pypi.python.org/pypi/PyUtilib) to declare a series of interfaces and extension points that then are used by plugins to hook in. It also implements a series of [Jinja2]( http://jinja.pocoo.org/) extension (notably CKAN_EXTENDS) that allows easily template inheritance between CKAN and connected plugins.

CKAN however is developed using [Pylons](http://pylonsproject.org/about-pylons-framework.html) which is now superseded by Pyramid and coupled to its complexity makes it difficult to grasp how to apply such extensibility to Pyramid web applications.

This example applies a modified version of CKAN extensible system to a simple Pyramid application that can be used as a starter to develop more complex extendable web applications. The example (pcaexample )is based on a “pyramid-cookiecutter-alchemy” Cookiecutter while the plugin is based on a “pyramid-cookiecutter-starter”. It uses Pyramid 1.8 with PyUtilib 5.4.1.

## Installation and testing
To build and run the example host application (pcaexample) on Linux do:

    $ git git@github.com:qlands/pyramid-pca-jinja2.git
    $ virtualenv pcaexample_env
    $ . ./pcaexample_env/bin/activate
    $ cd pyramid-pca-jinja2
    $ cd pcaexample
    $ python setup.py install
    $ pserve ./development.init

To build the a example of the plugin (pcaplugin) on Linux do:

    $ cd pyramid-pca-jinja2
    $ cd pcaplugin
    $ python setup.py develop
    $ cd ..
    $ cd pcaexample


Edit the configuration of the host application (development.ini) to load the plugin by **uncommenting line 20**.
> #pcaexample.plugins = examplePlugin -> pcaexample.plugins = examplePlugin

Then do:

    $ pserve ./development.init

## Author
Carlos Quiros (cquiros_at_qlands.com / c.f.quiros_at_cgiar.org)