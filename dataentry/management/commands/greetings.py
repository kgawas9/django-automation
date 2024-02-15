from typing import Any
from django.core.management.base import BaseCommand, CommandParser


class Command(BaseCommand):
    """To greet the user."""

    help = "Greet the user."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('name', type=str, help='Specifies user name.')

    def handle(self, *args: Any, **options: Any):
        """Business logic of Greeting."""

        self.stdout.write(self.style.SUCCESS(f"Hello {options.get('name', 'Anonymous User')}, welcome to automation project."))
