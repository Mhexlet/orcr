from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from datetime import datetime, timedelta
import pytz
from django.conf import settings


class FieldOfActivity(models.Model):

    name = models.CharField(max_length=64, verbose_name='Название')

    class Meta:
        verbose_name = 'Сфера деятельности'
        verbose_name_plural = 'Сферы деятельности'

    def __str__(self):
        return self.name


class User(AbstractUser):

    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=64, verbose_name='Имя')
    patronymic = models.CharField(max_length=64, verbose_name='Отчество')
    last_name = models.CharField(max_length=64, verbose_name='Фамилия')
    field_of_activity = models.ForeignKey(FieldOfActivity, on_delete=models.SET_NULL, null=True, verbose_name='Сфера деятельности')
    profession = models.CharField(max_length=64, verbose_name='Профессия')
    photo = models.ImageField(upload_to='profile_photos/', verbose_name='Фото')
    city = models.CharField(max_length=128, verbose_name='Город')
    birthdate = models.DateField(null=True, verbose_name='Дата рождения')
    workplace_address = models.CharField(max_length=128, verbose_name='Адрес места работы')
    workplace_name = models.CharField(max_length=128, verbose_name='Название места работы')
    phone_number = models.CharField(max_length=16, verbose_name='Номер рабочего телефона')
    description = models.TextField(verbose_name='О себе')
    registered = models.BooleanField(default=False, verbose_name='Реестровый специалист')
    approved = models.BooleanField(default=False, verbose_name='Одобрен')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def get_articles_count(self):
        return len(self.articles.select_related().filter(approved=True))

    @property
    def get_articles(self):
        return self.articles.select_related().filter(approved=True).order_by('-pk')

    @property
    def get_applications(self):
        return self.applications.select_related().order_by('-pk')

    def __str__(self):
        try:
            return f'{self.last_name} {str(self.first_name)[0]}. {str(self.patronymic)[0]}.'
        except IndexError:
            return self.username


class UserApprovalApplication(models.Model):

    user = models.ForeignKey(User, related_name='applications', on_delete=models.CASCADE, verbose_name='Специалист')
    time = models.DateTimeField(auto_now=True, verbose_name='Время создания')
    treated = models.BooleanField(default=False, verbose_name='Обработана')
    response = models.BooleanField(default=False, verbose_name='Вердикт')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')

    class Meta:
        verbose_name = 'Заявка на одобрение профиля'
        verbose_name_plural = 'Заявки на одобрение профиля'

    def __str__(self):
        return f'{self.user}'


@receiver(models.signals.pre_save, sender=UserApprovalApplication)
def approve_article(sender, instance, raw, using, update_fields, *args, **kwargs):
    if instance.response:
        instance.user.approved = True
        instance.user.approved_at = datetime.now()
        instance.user.save()
    if instance.response or instance.comment:
        instance.treated = True
