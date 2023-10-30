import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from datetime import datetime, timedelta
import pytz
from django_summernote.models import Attachment
from PIL import Image
from MedProject.settings import BASE_DIR
from django.conf import settings
import calendar
import time
from uuid import uuid4


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
    photo = models.ImageField(upload_to='tmp/', verbose_name='Фото')
    city = models.CharField(max_length=128, verbose_name='Город')
    birthdate = models.DateField(null=True, verbose_name='Дата рождения')
    workplace_address = models.CharField(max_length=128, verbose_name='Адрес места работы')
    workplace_name = models.CharField(max_length=128, verbose_name='Название места работы')
    phone_number = models.CharField(max_length=16, verbose_name='Номер рабочего телефона')
    description = models.TextField(verbose_name='О себе')
    registered = models.BooleanField(default=False, verbose_name='Реестровый специалист')
    approved = models.BooleanField(default=False, verbose_name='Одобрен')
    email_verified = models.BooleanField(default=True, verbose_name='Почта подтверждена')
    verification_key = models.CharField(max_length=128, blank=True, null=True, verbose_name='Ключ подтверждения почты')
    verification_key_expires = models.DateTimeField(blank=True, null=True, verbose_name='Ключ истекает')

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
    def get_open_articles(self):
        return self.articles.select_related().filter(approved=True, hidden=False).order_by('-pk')

    @property
    def get_applications(self):
        return self.approval_applications.select_related().order_by('-pk')

    @property
    def get_waiting_edits(self):
        return self.edit_applications.select_related().filter(treated=False).order_by('-pk')

    @property
    def get_rejected_edits(self):
        return self.edit_applications.select_related().filter(treated=True, response=False).order_by('-pk')

    @property
    def get_birthdate(self):
        return self.birthdate.strftime("%d-%m-%Y")

    @property
    def application_exists(self):
        return UserApprovalApplication.objects.filter(treated=False).exists()

    @property
    def is_verification_key_expired(self):
        if datetime.now(pytz.timezone(settings.TIME_ZONE)) > self.verification_key_expires + timedelta(hours=48):
            return True
        return False

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
    verbose_field = models.CharField(max_length=32, null=True, verbose_name='Поле')
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

    @property
    def get_value(self):
        if self.field == 'field_of_activity':
            return self.new_value[self.new_value.find("|") + 1:]
        else:
            return self.new_value


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
            instance.user.photo = instance.new_value
        elif instance.field == 'birthdate':
            instance.user.birthdate = f'{instance.new_value[6:]}-{instance.new_value[3:5]}-{instance.new_value[:2]}'
        else:
            setattr(instance.user, instance.field, instance.new_value)
        instance.user.save()
    if instance.response or instance.comment:
        instance.treated = True


@receiver(models.signals.pre_delete, sender=User)
def delete_user_photo(sender, instance, using, origin, **kwargs):
    try:
        os.remove(os.path.join(BASE_DIR, 'media', instance.photo.name))
    except FileNotFoundError:
        pass


@receiver(models.signals.pre_save, sender=Attachment)
def compress_attachment(sender, instance, **kwargs):
    file = instance.file.name
    ext = f'.{file.split(".")[-1]}'
    exts = Image.registered_extensions()
    supported_extensions = {ex for ex, f in exts.items() if f in Image.OPEN}
    if ext in supported_extensions:
        img = Image.open(instance.file)
        current_gmt = time.gmtime()
        time_stamp = calendar.timegm(current_gmt)
        file_name = f'{time_stamp}-{uuid4().hex}.jpg'
        new_file_path = os.path.join(BASE_DIR, 'media', 'attachments', file_name)
        width = img.size[0]
        height = img.size[1]
        ratio = width / height
        if ratio > 1 and width > 1024:
            sizes = [1024, int(1024 / ratio)]
            img = img.resize(sizes)
        elif height > 1024:
            sizes = [int(1024 * ratio), 1024]
            img = img.resize(sizes)
        try:
            img.save(new_file_path, quality=90, optimize=True)
        except OSError:
            img = img.convert("RGB")
            img.save(new_file_path, quality=90, optimize=True)
        instance.file = f'attachments/{file_name}'
