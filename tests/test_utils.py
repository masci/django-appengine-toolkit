from django.test import TestCase

import StringIO

import mock

from appengine_toolkit.management.commands._utils import collect_dependency_paths
from appengine_toolkit.management.commands._utils import parse_requirements_file
from appengine_toolkit.management.commands._utils import RequirementNotFoundError


class TestUtils(TestCase):
    def test_collect_dependency_paths(self):
        with mock.patch('pkg_resources.get_distribution') as mock_get_d, \
            mock.patch('os.path.isdir') as mock_isdir, mock.patch('os.path.exists'):
            dist = mock_get_d.return_value
            dist.has_metadata.return_value = True
            dist.get_metadata.return_value = 'foo\nfoo/bar\n'
            dist.location = ''
            req = mock.MagicMock()
            req.project_name = 'baz'
            dist.requires.side_effect = [[req], []]
            mock_isdir.return_value = False
            deps = collect_dependency_paths('foo')
            self.assertEqual(2, len(deps))
            self.assertTrue('foo.py' in deps)

    def test_collect_dependency_paths_fail(self):
        self.assertRaises(RequirementNotFoundError, collect_dependency_paths, 'foo')
        self.assertRaises(RequirementNotFoundError, collect_dependency_paths, 'wrong/foo')

    def test_parse_requirements_file(self):
        input = """
        django<1.6

        # comment
          # another comment
        """
        infile = StringIO.StringIO()
        infile.write(input)
        infile.seek(0)
        lines = parse_requirements_file(infile)
        self.assertEqual(1, len(lines))
        self.assertTrue('django' in lines[0])
