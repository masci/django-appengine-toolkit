from django.test import TestCase
from django.core.management import call_command, CommandError

import os

import mock

from appengine_toolkit.settings import appengine_toolkit_settings


class TestCommands(TestCase):
    def tearDown(self):
        appengine_config = os.path.join(os.path.dirname(appengine_toolkit_settings.APP_YAML), 'appengine_config.py')
        if os.path.exists(appengine_config):
            os.remove(appengine_config)


class TestCollectDeps(TestCommands):
    def test_call_wrong(self):
        self.assertRaises(CommandError, call_command, 'collectdeps', interactive=False)

    def test_call_package(self):
        with mock.patch('appengine_toolkit.management.commands.collectdeps.collect_dependency_paths') as mock_collect:
            mock_collect.return_value = []
            call_command('collectdeps', 'foo', interactive=False)
            self.assertEqual(mock_collect.call_args[0], ('foo',))

    def test_call_req_file(self):
        with mock.patch('__builtin__.open'), \
                mock.patch('appengine_toolkit.management.commands.collectdeps.parse_requirements_file') as mock_parse, \
                mock.patch('appengine_toolkit.management.commands.collectdeps.collect_dependency_paths') as mock_collect:
            mock_parse.return_value = ['foo']
            mock_collect.return_value = []
            call_command('collectdeps', requirements_file='foofile', interactive=False)

    def test_call_req_file_fail(self):
        with mock.patch('__builtin__.open'), \
                mock.patch('appengine_toolkit.management.commands.collectdeps.parse_requirements_file') as mock_parse:#, \
            mock_parse.return_value = ['foo']
            self.assertRaises(CommandError, call_command, 'collectdeps', requirements_file='foofile', interactive=False)

    def test_call_create_deps_dir(self):
        with mock.patch('appengine_toolkit.management.commands.collectdeps.os.path.exists') as mock_exists,\
            mock.patch('appengine_toolkit.management.commands.collectdeps.os.mkdir') as mock_mkdir,\
            mock.patch('appengine_toolkit.management.commands.collectdeps.collect_dependency_paths'):
            mock_exists.return_value = False
            call_command('collectdeps', 'foo', interactive=False)
            self.assertTrue('/libs' in mock_mkdir.call_args[0][0])