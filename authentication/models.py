from django.db import models
from django.contrib.auth.models import AbstractUser


class FieldOfActivity(models.Model):

    name = models.CharField(max_length=64, verbose_name='Название')

    class Meta:
        verbose_name = 'Сфера деятельности'
        verbose_name_plural = 'Сферы деятельности'


class User(AbstractUser):

    first_name = models.CharField(max_length=64, verbose_name='Имя')
    patronymic = models.CharField(max_length=64, verbose_name='Отчество')
    last_name = models.CharField(max_length=64, verbose_name='Фамилия')
    field_of_activity = models.ForeignKey(FieldOfActivity, on_delete=models.SET_NULL, null=True, verbose_name='Сфера деятельности')
    profession = models.CharField(max_length=64, verbose_name='Профессия')
    photo = models.ImageField(upload_to='profile_photos/', verbose_name='Фото')
    city = models.CharField(max_length=128, verbose_name='Город')
    birthdate = models.IntegerField(null=True, verbose_name='Дата рождения')
    workplace_address = models.CharField(max_length=128, verbose_name='Адрес места работы')
    workplace_name = models.CharField(max_length=128, verbose_name='Название места работы')
    phone_number = models.CharField(max_length=16, verbose_name='Номер рабочего телефона')
    description = models.TextField(verbose_name='О себе')
    registered = models.BooleanField(default=False, verbose_name='Реестровый специалист')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def get_articles_count(self):
        return self.articles.select_related()


