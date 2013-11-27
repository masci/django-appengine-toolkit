import sys
import os
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from ._utils import collect_dependency_paths, parse_requirements_file, RequirementNotFoundError, make_simlinks
from ...settings import  appengine_toolkit_settings


class Command(BaseCommand):
    args = "<package_name package_name ...>"
    help = "make symlinks to project dependencies"

    option_list = BaseCommand.option_list + (
        make_option(
            '-r',
            '--requirements',
            action='store',
            dest='requirements_file',
            help='Collect dependencies for packages contained in requirement file'
        ),
    )

    def handle(self, *args, **options):
        req_file_path = options.get('requirements_file')
        if not len(args) and not req_file_path:
            raise CommandError('Please provide at least a package name or a requirement file\n')

        deps = []

        sys.stdout.write('Collecting dependencies...\n')
        if req_file_path:
            with open(req_file_path) as f:
                for line in parse_requirements_file(f):
                    try:
                        deps.extend(collect_dependency_paths(line))
                    except RequirementNotFoundError as e:
                        raise CommandError('Error processing requirement file: {}\n'.format(e))

        for package in args:
            deps.extend(collect_dependency_paths(package))

        deps = set(deps)

        sys.stdout.write('{} dependencies found...\n'.format(len(deps)))

        sys.stdout.write('Making symlinks...\n')
        if not os.path.exists(appengine_toolkit_settings.DEPENDENCIES_ROOT):
            os.mkdir(appengine_toolkit_settings.DEPENDENCIES_ROOT)
        make_simlinks(appengine_toolkit_settings.DEPENDENCIES_ROOT, deps)

        sys.stdout.write('All done.\n')
