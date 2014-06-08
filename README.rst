=============================
Django Appengine Toolkit
=============================

.. image:: https://badge.fury.io/py/django-appengine-toolkit.png
    :target: http://badge.fury.io/py/django-appengine-toolkit
    
.. image:: https://travis-ci.org/masci/django-appengine-toolkit.png?branch=master
        :target: https://travis-ci.org/masci/django-appengine-toolkit

.. image:: https://pypip.in/d/django-appengine-toolkit/badge.png
        :target: https://crate.io/packages/django-appengine-toolkit?version=latest

.. image:: https://coveralls.io/repos/masci/django-appengine-toolkit/badge.png
        :target: https://coveralls.io/r/masci/django-appengine-toolkit

Appengine Toolkit pimps Django with some utilities that help deploying
projects on Google App Engine with Google Cloud SQL as data backend.

Features
--------

* collects project dependencies symlinking needed modules and packages and configuring App Engine environment
* configures DATABASE setting parsing connection strings similar to those on Heroku
* provides a custom storage for Google Cloud Storage

Documentation
-------------

The full documentation is at http://django-appengine-toolkit.rtfd.org.

A tutorial was published on `Google Developers Blog <http://googledevelopers.blogspot.it/2014/02/create-blog-on-app-engine-with-django.html>`_

Another `how-to upload to cloud storage <https://github.com/masci/django_cloudstorage_example>`_

AppEngine SDK version supported: 1.9.4

Quickstart
----------

Install appengine-toolkit::

    pip install django-appengine-toolkit

Add it to the installed apps::

    INSTALLED_APPS = (
        # ...
        'appengine_toolkit',
    )

To automatically configure database settings by parsing connection string
contained in DATABASE_URL enviroment var::

    import appengine_toolkit
    DATABASES = {
        'default': appengine_toolkit.config(),
    }

You can set DATABASE_URL directly in your ``app.yaml`` file::

    env_variables:
      DJANGO_SETTINGS_MODULE: 'myapp.settings'
      DATABASE_URL: 'mysql://root@project_id:instance_id/database_name'


To collect project dependencies, first configure Appengine Toolkit specifying the full 
path pointing to the app.yaml file in your `settings.py` module::

    APPENGINE_TOOLKIT = {
        'APP_YAML': os.path.join(BASE_DIR, '../../', 'app.yaml'),
    }


...then run the command ``collectdeps`` specifying the requirement file containing
the list of packages needed by your project to run::

    python manage.py collectdeps -r my_requirements.txt

a folder named ``libs`` will be created on your application root (i.e. the same folder
where the YAML file resides) containing symlinks needed by App Engine to include
dependencies in the production runtime enviroment.

A file ``appengine_config.py`` will be created in the same folder and will contain
code needed to configure the environment. If you need to customize the module
``appengine_config`` tell the command to not overwrite it - the command will then
output the code you need to paste inside the module to complete the configuration
process

Need to store your media files on Google Cloud Storage? Just add this to your settings::

    APPENGINE_TOOLKIT = {
        # ...,
        'BUCKET_NAME': 'your-bucket-name',
    }
    DEFAULT_FILE_STORAGE = 'appengine_toolkit.storage.GoogleCloudStorage'

