from django.contrib import admin
from .models import Section, Page, AlbumBlock, FileSetBlock, AlbumImage, FileSetFile
from django.db.models.fields.reverse_related import ManyToOneRel
from django_summernote.admin import SummernoteModelAdmin


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


@admin.register(FileSetFile)
class FileSetFileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FileSetFile._meta.get_fields()]


@admin.register(Page)
class PageAdmin(SummernoteModelAdmin):
    # displaying posts with title slug and created time
    list_display = [field.name for field in Page._meta.get_fields() if type(field) != ManyToOneRel]
    list_filter = ('title', 'url', 'section')
    search_fields = ['title', 'url', 'section']
    # prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)

