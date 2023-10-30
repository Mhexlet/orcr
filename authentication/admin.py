import os
import shutil

from PIL import Image
from django.contrib import admin
from MedProject.settings import BASE_DIR
from .models import FieldOfActivity, User, UserApprovalApplication, UserEditApplication
from django.db.models.fields.reverse_related import ManyToOneRel
import calendar
import time
from uuid import uuid4


def compress_img(instance, field, directory, multiple=True):
    file = getattr(instance, field)
    print(file)
    print(file.name)
    img = Image.open(file)
    current_gmt = time.gmtime()
    time_stamp = calendar.timegm(current_gmt)
    file_name = f'{time_stamp}-{uuid4().hex}.jpg'
    new_file_path = os.path.join(BASE_DIR, 'media', directory, file_name)
    print(new_file_path)
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
        if change and 'photo' in form.changed_data:
            compress_img(form.instance, 'photo', 'profile_photos')
        return super(UserAdmin, self).save_model(request, obj, form, change)


@admin.register(UserApprovalApplication)
class UserApprovalApplicationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserApprovalApplication._meta.get_fields()]
    exclude = ('field',)


@admin.register(UserEditApplication)
class UserEditApplicationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserEditApplication._meta.get_fields()]
