from django.test import TestCase
from django.core.management import call_command


class TestCommands(TestCase):
    pass


class TestCollectDeps(TestCommands):
    def test_call(self):
        #call_command('collectdeps', requirements_file='requirements-test.txt')
        pass
