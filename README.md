# An extendable Pyramid application using PCA and Jinja2 plugins

[Pyramid]( https://trypyramid.com/) is a great framework for developing web applications that also supports the development of ["Extensible" and "Pluggable"]( http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/extending.html) software based on certain rules. However, there is no much documentation on how to create such type of applications.

[CKAN]( https://ckan.org/) is an excellent example of a Web application that can be extended or customized using plug-ins. It relies on [PyUtilib Component Architecture]( https://pypi.python.org/pypi/PyUtilib) to declare a series of interfaces and extension points that then are used by plug-ins to hook in. It also implements a series of [Jinja2]( http://jinja.pocoo.org/) extension (notably CKAN_EXTENDS) that allows easily template inheritance between CKAN and connected plug-ins.

CKAN however was developed using [Pylons](http://pylonsproject.org/about-pylons-framework.html) which is now superseded by Pyramid and coupled to its complexity makes it difficult to grasp how to apply such extensibility to Pyramid web applications.

This example applies a modified version of CKAN extensible system to a simple Pyramid application that can be used as a starting point to develop more complex extendable web applications. The example allows plug-ins to extend the host by:
 - Adding new routes
 - Adding and overwriting templates
 - Adding new static resources
 - Adding new JSS or CSS resources
 - Easy Jinja2 template inheritance and resource injection


The example (pcaexample) is based on a “pyramid-cookiecutter-alchemy” [Cookiecutter](https://github.com/audreyr/cookiecutter) while the plug-in is based on a “pyramid-cookiecutter-starter”.  Both use Python 3.

Please note that this example implements Pyramid "Extensible" and "Pluggable" capabilities in a way that I feel it would satisfy most needs. I don't claim is the best nor the most logical way of doing it.  See [FormShare](https://github.com/qlands/FormShare) for a real example of this approach.

**Comments and suggestions are welcomed.**

## Installation and testing
To build and run the example host application (pcaexample) on Linux do:

```shell
git clone https://github.com/qlands/pyramid-pca-jinja2.git
python3 -m venv pcaexample_env
source ./pcaexample_env/bin/activate
cd pyramid-pca-jinja2
cd pcaexample
python setup.py install
initialize_pcaexample_db ./development.ini
pserve ./development.ini
```

To build the a example of the plugin (pcaplugin) on Linux do:

```shell
cd pyramid-pca-jinja2
cd pcaplugin
python setup.py develop
cd ..
cd pcaexample
```


Edit the configuration of the host application (development.ini) to load the plug-in by **uncommenting line 26** to read:
> pcaexample.plugins = examplePlugin

Then do:

```shell
pserve ./development.ini
```

## Screenshot

![Image](/screenshot.png?raw=true "Example home screen with and without plugin")


## Author
Carlos Quiros (cquiros_at_qlands.com / c.f.quiros_at_cgiar.org)