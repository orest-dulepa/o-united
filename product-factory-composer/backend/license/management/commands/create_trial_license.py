import os
from django.core.management.base import BaseCommand

from license.models import License


class Command(BaseCommand):
    help = "Requests trial license, eliminates need to enter license key manually in the UI"

    def handle(self, *args, **options):
        if License.objects.count() > 0:
            print("This OU instance already has a license")
            return

        raw_license_data = os.environ.get("LICENSE_TRIAL_KEY", "")
        if not raw_license_data:
            print("The license trial key is empty")
            return
        License.objects.create(license_data=raw_license_data, current=True)

        print("License successfully created")

