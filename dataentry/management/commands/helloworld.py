from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Create a custom commands."""
    help = "helloworld command is going to print Hello World."

    def handle(self, *args, **kwargs):
        """Logic of the helloworld custom command goes here."""
        # write the logic here.
        self.stdout.write("Custom command 'helloworld' executed. the output is Hello world.")
