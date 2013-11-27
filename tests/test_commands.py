from django.test import TestCase
from django.core.management import call_command, CommandError

import mock


class TestCommands(TestCase):
    pass


class TestCollectDeps(TestCommands):
    def test_call_wrong(self):
        self.assertRaises(CommandError, call_command, 'collectdeps')

    def test_call_package(self):
        with mock.patch('appengine_toolkit.management.commands.collectdeps.collect_dependency_paths') as mock_collect:
            mock_collect.return_value = []
            call_command('collectdeps', 'foo')
            self.assertEqual(mock_collect.call_args[0], ('foo',))

    def test_call_req_file(self):
        with mock.patch('__builtin__.open'), \
                mock.patch('appengine_toolkit.management.commands.collectdeps.parse_requirements_file') as mock_parse, \
                mock.patch('appengine_toolkit.management.commands.collectdeps.collect_dependency_paths') as mock_collect:
            mock_parse.return_value = ['foo']
            mock_collect.return_value = []
            call_command('collectdeps', requirements_file='foofile')

    def test_call_req_file_fail(self):
        with mock.patch('__builtin__.open'), \
                mock.patch('appengine_toolkit.management.commands.collectdeps.parse_requirements_file') as mock_parse:#, \
                #mock.patch('appengine_toolkit.management.commands.collectdeps.collect_dependency_paths') as mock_collect:
            mock_parse.return_value = ['foo']
            #mock_collect.return_value = ['foo']
            self.assertRaises(CommandError, call_command, 'collectdeps', requirements_file='foofile')
