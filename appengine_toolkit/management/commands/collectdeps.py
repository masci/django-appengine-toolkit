import sys
import os
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.utils.six.moves import input

from ._utils import collect_dependency_paths, parse_requirements_file, make_simlinks, get_config_code
from ._utils import RequirementNotFoundError
from ...settings import appengine_toolkit_settings


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
        make_option(
            '--noinput',
            action='store_false',
            dest='interactive',
            default=True,
            help='Tells Django to NOT prompt the user for input of any kind.'
        ),
    )

    def handle(self, *args, **options):
        interactive = options.get('interactive', True)
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

        app_root = os.path.dirname(appengine_toolkit_settings.APP_YAML)
        deps_root = os.path.join(app_root, appengine_toolkit_settings.DEPENDENCIES_ROOT)

        if not os.path.exists(deps_root):
            sys.stdout.write('Creating dependencies root folder...\n')
            os.mkdir(deps_root)
        make_simlinks(deps_root, deps)

        sys.stdout.write('Writing config to appengine_config.py...\n')

        appengine_config = os.path.join(app_root, 'appengine_config.py')

        write_file = True
        if interactive and os.path.exists(appengine_config):
            msg = ("\nA file called appengine_config.py already exist at "
                   "application root path.\nWould you like to overwrite it? (yes/no): ")
            confirm = input(msg)
            while 1:
                if confirm not in ('yes', 'no'):
                    confirm = input('Please enter either "yes" or "no": ')
                    continue
                if confirm == 'no':
                    write_file = False
                break

        msg = get_config_code(appengine_toolkit_settings.DEPENDENCIES_ROOT)
        if write_file:
            with open(os.path.join(app_root, 'appengine_config.py'), 'w') as f:
                f.write(msg)
        else:
            sys.stdout.write('Please ensure your appengine_config.py contains the following:\n\n')
            sys.stdout.write(msg)
            sys.stdout.write('\n')

        sys.stdout.write('All done.\n')
