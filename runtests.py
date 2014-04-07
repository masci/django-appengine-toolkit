import sys
import os
from optparse import OptionParser

import google

here = os.path.dirname(os.path.abspath(__file__))
gae_path = os.path.dirname(os.path.abspath(google.__file__))
dir_path = os.path.join(gae_path, '..')

GAE_LIBRARY_PATHS = [
    dir_path,
    os.path.join(dir_path, 'lib', 'cherrypy'),
    os.path.join(dir_path, 'lib', 'fancy_urllib'),
    os.path.join(dir_path, 'lib', 'yaml-3.10'),
    os.path.join(dir_path, 'lib', 'antlr3'),
    os.path.join(dir_path, 'lib', 'concurrent'),
    os.path.join(dir_path, 'lib', 'ipaddr'),
    os.path.join(dir_path, 'lib', 'jinja2-2.6'),
    os.path.join(dir_path, 'lib', 'webob-1.2.3'),
    os.path.join(dir_path, 'lib', 'webapp2-2.5.1'),
    os.path.join(dir_path, 'lib', 'mox'),
    os.path.join(dir_path, 'lib', 'protorpc-1.0'),
    os.path.join(dir_path, 'lib', 'simplejson'),
]

try:
    from django.conf import settings

    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            }
        },
        ROOT_URLCONF="appengine_toolkit.urls",
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            "appengine_toolkit",
        ],
        SITE_ID=1,
        NOSE_ARGS=['-s'],
        APPENGINE_TOOLKIT={
            'APP_YAML': os.path.join(here, 'tests', 'foo.yaml'),
            'BUCKET_NAME': 'test_bucket',
        },
        DEFAULT_FILE_STORAGE='appengine_toolkit.storage.GoogleCloudStorage',
    )

    from django_nose import NoseTestSuiteRunner
except ImportError:
    raise ImportError("To fix this error, run: pip install -r requirements-test.txt")


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    # Run tests
    test_runner = NoseTestSuiteRunner(verbosity=1)

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(failures)


if __name__ == '__main__':
    sys.path.extend(GAE_LIBRARY_PATHS)

    from google.appengine.tools import old_dev_appserver
    from google.appengine.tools.dev_appserver_main import ParseArguments

    option_dict = ParseArguments(sys.argv)[1]
    old_dev_appserver.SetupStubs('local', **option_dict)

    parser = OptionParser()
    (options, args) = parser.parse_args()
    run_tests(*args)