import sys
import os
from optparse import OptionParser

here = os.path.dirname(os.path.abspath(__file__))

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
        }
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
    parser = OptionParser()
    (options, args) = parser.parse_args()
    run_tests(*args)