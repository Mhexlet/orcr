from django.contrib import admin
from .models import FieldOfActivity, User
from django.db.models.fields.related import ManyToManyField
from django.db.models.fields.reverse_related import ManyToOneRel


@admin.register(FieldOfActivity)
class FieldOfActivityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FieldOfActivity._meta.get_fields() if type(field) != ManyToOneRel]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in User._meta.get_fields() if type(field) not in [ManyToManyField, ManyToOneRel]]
