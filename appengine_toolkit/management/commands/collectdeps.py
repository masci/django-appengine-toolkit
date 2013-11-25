import sys

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from optparse import make_option

from ._utils import collect_dependency_paths, RequirementNotFoundError


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
        deps = []

        req_file = options.get('requirements_file')
        if req_file:
            with open(req_file) as f:
                for line in (x.strip() for x in f.readlines()):
                    if not line or line.startswith('#'):
                        continue
                    try:
                        deps.extend(collect_dependency_paths(line))
                    except RequirementNotFoundError as e:
                        sys.stderr.write('Error processing requirement file: {}\n'.format(e))

        for package in args:
            deps.extend(collect_dependency_paths(package))

        deps = set(deps)

        for dep in deps:
            sys.stderr.write(dep+'\n')
