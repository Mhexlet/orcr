from django.core.management.base import BaseCommand
from main.models import SiteContent


class Command(BaseCommand):

    def handle(self, *args, **options):

        try:
            SiteContent.objects.create(name='phone', content='+7 (900) 999-99-99')
            SiteContent.objects.create(name='email', content='example@gmail.com')
        except:
            pass