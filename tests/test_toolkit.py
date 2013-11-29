from django.test import TestCase

import os
import mock

from appengine_toolkit import on_appengine, config, parse


class TestToolkit(TestCase):
    def test_on_appengine(self):
        self.assertFalse(on_appengine())
        os.environ['SERVER_SOFTWARE'] = 'Google App Engine Fake'
        self.assertTrue(on_appengine())
        del os.environ['SERVER_SOFTWARE']

    def test_config(self):
        with mock.patch('appengine_toolkit.parse') as mock_parse:
            env_var = 'FOO_ENVVAR'
            os.environ[env_var] = 'Foo'
            config(env_var)
            self.assertEqual(mock_parse.call_args[0], ('Foo',))
            del os.environ[env_var]

    def test_parse_wrong_string(self):
        dbconf = parse("foo://bar:baz@foo:8080/url")
        self.assertFalse('ENGINE' in dbconf)

    def test_parse_local_db_string(self):
        dbconf = parse("mysql://root:pass@localhost:3306/dbname")
        expected = {
            'NAME': 'dbname',
            'USER': 'root',
            'PASSWORD': 'pass',
            'HOST': 'localhost',
            'PORT': 3306,
            'ENGINE': 'django.db.backends.mysql',
        }
        self.assertEqual(dbconf, expected)

    def test_parse_cloudsql_string(self):
        dbconf = parse("mysql://root:pass@project:instance/dbname")
        expected = {
            'NAME': 'dbname',
            'USER': 'root',
            'PASSWORD': 'pass',
            'HOST': '/cloudsql/project:instance',
            'PORT': None,
            'ENGINE': 'django.db.backends.mysql',
        }
        self.assertEqual(dbconf, expected)

    def test_parse_cloudsql_local(self):
        dbconf = parse("rdbms://root:pass@project:instance/dbname")
        expected = {
            'NAME': 'dbname',
            'USER': 'root',
            'PASSWORD': 'pass',
            'HOST': None,
            'INSTANCE': 'project:instance',
            'PORT': None,
            'ENGINE': 'google.appengine.ext.django.backends.rdbms',
        }
        self.assertEqual(dbconf, expected)
