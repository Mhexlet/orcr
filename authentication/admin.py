import os
import shutil
from django.utils.html import format_html
from PIL import Image
from django.contrib import admin
from MedProject.settings import BASE_DIR, BASE_URL
from .models import FieldOfActivity, User, UserApprovalApplication, UserEditApplication
from django.db.models.fields.reverse_related import ManyToOneRel
import calendar
import time
from uuid import uuid4


def compress_img(instance, field, directory, multiple=True):
    file = getattr(instance, field)
    img = Image.open(file)
    current_gmt = time.gmtime()
    time_stamp = calendar.timegm(current_gmt)
    file_name = f'{time_stamp}-{uuid4().hex}.jpg'
    new_file_path = os.path.join(BASE_DIR, 'media', directory, file_name)
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
    if multiple:
        try:
            shutil.rmtree(os.path.join(BASE_DIR, 'media', 'tmp'))
        except (FileNotFoundError, PermissionError):
            pass
        os.mkdir(os.path.join(BASE_DIR, 'media', 'tmp'))
    setattr(instance, field, os.path.join(directory, file_name))


@admin.register(FieldOfActivity)
class FieldOfActivityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FieldOfActivity._meta.get_fields() if type(field) != ManyToOneRel]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'last_login', 'first_name', 'patronymic', 'last_name', 'birthdate',
                    'field_of_activity', 'profession', 'city', 'workplace_address', 'workplace_name',
                    'phone_number', 'email', 'photo', 'short_description', 'email_verified']
    exclude = ('groups', 'is_superuser', 'is_staff', 'user_permissions', 'password', 'verification_key',
               'verification_key_expires')

    def short_description(self, obj):
        return obj.description[:50] + '...'

    short_description.short_description = 'О себе'

    def save_model(self, request, obj, form, change):
        if not change or (change and 'photo' in form.changed_data):
            if change:
                try:
                    os.remove(os.path.join(BASE_DIR, 'media', form.initial['photo'].name))
                except FileNotFoundError:
                    pass
            compress_img(form.instance, 'photo', 'profile_photos')
        return super(UserAdmin, self).save_model(request, obj, form, change)


@admin.register(UserApprovalApplication)
class UserApprovalApplicationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserApprovalApplication._meta.get_fields()]


@admin.register(UserEditApplication)
class UserEditApplicationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserEditApplication._meta.get_fields()]
    exclude = ('field', 'new_value', 'old_value')
    readonly_fields = ['user', 'verbose_field', 'old_value_changed', 'new_value_changed']
    fields = ['user', 'verbose_field', 'old_value_changed', 'new_value_changed', 'treated', 'response', 'comment']

    def new_value_changed(self, obj):
        if obj.field == 'photo':
            url = f'{BASE_URL}/media/{obj.new_value}'
            return format_html(f"<img src='{url}' style='max-width: 300px; max-height: 300px;'>")
        else:
            return obj.new_value

    def old_value_changed(self, obj):
        if obj.field == 'photo':
            url = f'{BASE_URL}/media/{obj.old_value}'
            return format_html(f"<img src='{url}' style='max-width: 300px; max-height: 300px;'>")
        else:
            return obj.old_value

    old_value_changed.short_description = 'Старое значение'
    new_value_changed.short_description = 'Новое значение'

