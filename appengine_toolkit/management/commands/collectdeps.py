from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    args = "<requirement_file>"
    help = "make symlinks to project dependencies"

    def handle(self, *args, **options):
        raise CommandError("Not yet implemented!")
