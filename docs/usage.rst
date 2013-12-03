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

TODO::

	import django-appengine-toolkit