from django.contrib import admin
from .models import FieldOfActivity, User, UserApprovalApplication, UserEditApplication
from django.db.models.fields.reverse_related import ManyToOneRel


@admin.register(FieldOfActivity)
class FieldOfActivityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FieldOfActivity._meta.get_fields() if type(field) != ManyToOneRel]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'last_login', 'first_name', 'patronymic', 'last_name', 'birthdate',
                    'field_of_activity', 'profession', 'city', 'workplace_address', 'workplace_name',
                    'phone_number', 'email', 'photo', 'short_description']
    exclude = ('groups', 'is_superuser', 'is_staff', 'user_permissions', 'password',)

    def short_description(self, obj):
        return obj.description[:50] + '...'

    short_description.short_description = 'О себе'


@admin.register(UserApprovalApplication)
class UserApprovalApplicationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserApprovalApplication._meta.get_fields()]


@admin.register(UserEditApplication)
class UserEditApplicationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserEditApplication._meta.get_fields()]
