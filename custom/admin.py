import shutil

from django.contrib import admin

from authentication.admin import compress_img
from .models import Section, Page, AlbumBlock, FileSetBlock, AlbumImage, FileSetFile
from django.db.models.fields.reverse_related import ManyToOneRel
from django_summernote.admin import SummernoteModelAdmin
from MedProject.settings import BASE_DIR
import os


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Section._meta.get_fields() if type(field) != ManyToOneRel]


# @admin.register(Page)
# class PageAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in Page._meta.get_fields() if type(field) != ManyToOneRel]


# @admin.register(TextBlock)
# class TextBlockAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in TextBlock._meta.get_fields() if type(field) != ManyToOneRel]
#
#
# @admin.register(ImageBlock)
# class ImageBlockAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in ImageBlock._meta.get_fields() if type(field) != ManyToOneRel]
#
#
# @admin.register(MapBlock)
# class MapBlockAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in MapBlock._meta.get_fields() if type(field) != ManyToOneRel]
#
#
# @admin.register(HTMLBlock)
# class HTMLBlockAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in HTMLBlock._meta.get_fields() if type(field) != ManyToOneRel]


@admin.register(AlbumBlock)
class AlbumBlockAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AlbumBlock._meta.get_fields() if type(field) != ManyToOneRel]


@admin.register(FileSetBlock)
class FileSetBlockAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FileSetBlock._meta.get_fields() if type(field) != ManyToOneRel]


@admin.register(AlbumImage)
class AlbumImageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AlbumImage._meta.get_fields()]

    def save_model(self, request, obj, form, change):
        if not change or (change and 'image' in form.changed_data):
            compress_img(form.instance, 'image', 'images')
        return super(AlbumImageAdmin, self).save_model(request, obj, form, change)


@admin.register(FileSetFile)
class FileSetFileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FileSetFile._meta.get_fields()]


@admin.register(Page)
class PageAdmin(SummernoteModelAdmin):
    list_display = ['pk', 'title', 'url', 'section', 'short_content', 'approved']
    list_filter = ('title', 'url', 'section')
    search_fields = ['title', 'url', 'section']
    summernote_fields = ('content',)
    exclude = ('url',)

    def short_content(self, obj):
        return obj.content[:50] + '...'

    short_content.short_description = 'Содержимое'

    def save_model(self, request, obj, form, change):
        try:
            shutil.rmtree(os.path.join(BASE_DIR, 'media', 'django-summernote'))
        except (FileNotFoundError, PermissionError):
            pass
        return super().save_model(request, obj, form, change)

