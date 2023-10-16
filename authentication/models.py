import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from datetime import datetime, timedelta
import pytz


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
        return self.approval_applications.select_related().order_by('-pk')

    @property
    def get_birthdate(self):
        return self.birthdate.strftime("%d-%m-%Y")

    def __str__(self):
        try:
            return f'{self.last_name} {str(self.first_name)[0]}. {str(self.patronymic)[0]}.'
        except IndexError:
            return self.username


class UserApprovalApplication(models.Model):

    user = models.ForeignKey(User, related_name='approval_applications', on_delete=models.CASCADE, verbose_name='Специалист')
    time = models.DateTimeField(auto_now=True, verbose_name='Время создания')
    treated = models.BooleanField(default=False, verbose_name='Обработана')
    response = models.BooleanField(default=False, verbose_name='Вердикт')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')

    class Meta:
        verbose_name = 'Заявка на одобрение профиля'
        verbose_name_plural = 'Заявки на одобрение профиля'

    def __str__(self):
        return f'{self.user}'


class UserEditApplication(models.Model):

    user = models.ForeignKey(User, related_name='edit_applications', on_delete=models.CASCADE, verbose_name='Специалист')
    field = models.CharField(max_length=32, verbose_name='Поле')
    old_value = models.TextField(verbose_name='Старое значение')
    new_value = models.TextField(verbose_name='Новое значение')
    time = models.DateTimeField(auto_now=True, verbose_name='Время создания')
    treated = models.BooleanField(default=False, verbose_name='Обработана')
    response = models.BooleanField(default=False, verbose_name='Вердикт')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')

    class Meta:
        verbose_name = 'Заявка на изменение профиля'
        verbose_name_plural = 'Заявки на изменение профиля'

    def __str__(self):
        return f'{self.user} - {self.field}'


@receiver(models.signals.pre_save, sender=UserApprovalApplication)
def approve_user(sender, instance, raw, using, update_fields, *args, **kwargs):
    if instance.response:
        instance.user.approved = True
        instance.user.approved_at = datetime.now()
        instance.user.save()
    if instance.response or instance.comment:
        instance.treated = True


@receiver(models.signals.pre_save, sender=UserEditApplication)
def approve_edit(sender, instance, raw, using, update_fields, *args, **kwargs):
    if instance.response:
        if instance.field == 'field_of_activity':
            new_value = instance.new_value[instance.new_value.find(":") + 1:instance.new_value.find("|")]
            instance.user.field_of_activity = FieldOfActivity.objects.get(pk=int(new_value))
        elif instance.field == 'photo':
            instance.user.photo.name = instance.new_value
        elif instance.field == 'birthdate':
            instance.user.birthdate = f'{instance.new_value[6:]}-{instance.new_value[3:5]}-{instance.new_value[:2]}'
        else:
            setattr(instance.user, instance.field, instance.new_value)
        instance.user.save()
    if instance.response or instance.comment:
        instance.treated = True
