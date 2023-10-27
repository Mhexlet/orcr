from django.core.management.base import BaseCommand
from main.models import SiteContent


class Command(BaseCommand):

    def handle(self, *args, **options):

        try:
            SiteContent.objects.create(name='email_verification_message_beginning',
                                       content='Здравствуйте,\n\nПожалуйста, перейдите по ссылке, '
                                               'чтобы подтвердить свой адрес электронной почты:')
            SiteContent.objects.create(name='email_verification_message_ending', content='\n\nС уважением')
            SiteContent.objects.create(name='phone', content='+7 (900) 999-99-99')
            SiteContent.objects.create(name='email', content='example@gmail.com')
        except:
            pass