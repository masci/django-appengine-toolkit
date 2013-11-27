from django.test import TestCase

import StringIO
import os

import mock

from appengine_toolkit.management.commands._utils import collect_dependency_paths
from appengine_toolkit.management.commands._utils import parse_requirements_file
from appengine_toolkit.management.commands._utils import RequirementNotFoundError
from appengine_toolkit.management.commands._utils import make_simlinks


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

    def test_make_symlinks(self):
        with mock.patch('os.symlink') as mock_symlink:
            make_simlinks('/my/dest', ['/from/source_1', '/from/source_2'])
            calls = mock_symlink.call_args_list
            self.assertEqual(len(calls), 2)
            self.assertEqual(calls[0][0][1], '/my/dest/source_1')
            self.assertEqual(calls[1][0][1], '/my/dest/source_2')

    def test_make_symlinks_link_exists(self):
        with mock.patch('os.symlink'), mock.patch('os.path.islink'), \
             mock.patch('os.remove') as mock_remove:
            this = os.path.abspath(__file__)
            make_simlinks(os.path.dirname(this), [this])
            arg = mock_remove.call_args[0][0]
            self.assertEqual(arg, this)

    def test_make_symlink_path_exists(self):
        with mock.patch('os.symlink') as mock_symlink:
            this = os.path.abspath(__file__)
            make_simlinks(os.path.dirname(this), [this])
            self.assertEqual(0, mock_symlink.call_count)