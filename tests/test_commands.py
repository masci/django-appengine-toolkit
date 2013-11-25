from django.test import TestCase
from django.core.management import call_command


from appengine_toolkit.management.commands._utils import collect_dependency_paths


class TestUtils(TestCase):
    def test_collect_dependency_paths(self):
        self.assertEqual(1, len(collect_dependency_paths('django')))


class TestCommands(TestCase):
    pass


class TestCollectDeps(TestCommands):
    def test_call(self):
        call_command('collectdeps', requirements_file='requirements-test.txt')
