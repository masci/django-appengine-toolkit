Usage
=====

Collect project dependencies
----------------------------
Google App Engine does not provide a virtual environment where installing dependencies at deploy time, like Heroku does.
Dependencies must be present inside the application directory in the filesystem (i.e. where the ``.yaml`` file resides)
at the moment users deploy the application (either with the Google App Engine Launcher or with ``appcfg.py`` script
at the command line. Also, the path to the dependecies must be added to the ``sys.path`` so the Python runtime can
import them.

Both of those operations can be automated with App Engine Toolkit.

collectdeps <package_name ...>
+++++++++++
``python manage.py collectdeps``

Takes in input one or more package names (or a requirement file) and makes the symlink needed in the application directory
beside writing the code needed to adjust the ``sys.path`` in the ``appengine_config.py`` module. If the
``appengine_config.py`` is already present, the command prompts users whether they want to overwrite the file or print
needed python instructions in the terminal.

``--requirements requirements.txt``

Parse the list of dependencies from a requirement file

``--noinput``

Tells Django to NOT prompt the user for input of any kind.


Setup database configuration settings
-------------------------------------
At the moment, the only supported database backend for Django on App Engine is Google Cloud SQL, which
is basically a MySQL instance. You may configure a MySQL backend adding something like this
to your settings file::

    # a typical configuration to access a local MySQL instance
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': 'localhost',
            'NAME': 'django_test',
            'USER': 'root',
            'PASSWORD': 'secret',
        }
    }

using Google Cloud SQL is not very different indeed, but you have to compose the ``HOST`` string
carefully::

    # configuration needed to access a Google Cloud SQL instance
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '/cloudsql/your-project-id:your-instance-name',
            'NAME': 'django_test',
            'USER': 'root',
        }
    }

Django App Engine Toolkit makes things a lot simpler, provided that you set an environment
variable named ``DATABASE_URL`` following this schema::

    [database type]://[username]:[password]@[host]:[port]/[database name]

or, specifically for cloud SQL::

    [database type]://[username]:[password]@[project_id]:[instance_name]/[database name]

Once you defined such variable, just write this in your settings file::

    import appengine_toolkit
    DATABASES = {
        'default': appengine_toolkit.config(),
    }

You can set the ``DATABASE_URL`` env var in your ``app.yaml`` like this::

    env_variables:
      DATABASE_URL: 'mysql://root@my_project_id:my_instance_name/my_dbname'


If you want to work with the local development server but still accessing the remote Cloud SQL
instance, you can use the following ``DATABASE_URL`` string::

    'rdbms://root@my_project_id:my_instance_name/my_dbname'

To work with the local development server and a local MySQL instance, ``DATABASE_URL`` will look like::

    'mysql://root:password@localhost/my_dbname'
