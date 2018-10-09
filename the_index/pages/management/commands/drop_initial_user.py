from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseCommand):
    def handle(self, **options):
        try:
            User.objects.get(username='admin').delete()
        except ObjectDoesNotExist:
            print("Already Removed")
