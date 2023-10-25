from django.contrib import admin
from .models import Article, ArticleFile, ArticleApprovalApplication
from django.db.models.fields.reverse_related import ManyToOneRel
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):
    list_display = ['author', 'hidden', 'theme', 'title', 'short_text', 'created_at', 'approved_at', 'approved']
    summernote_fields = ('text',)

    def short_text(self, obj):
        return obj.text[:50] + '...'

    short_text.short_description = 'Текст'


@admin.register(ArticleFile)
class ArticleFileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ArticleFile._meta.get_fields()]


@admin.register(ArticleApprovalApplication)
class ArticleApprovalApplicationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ArticleApprovalApplication._meta.get_fields()]