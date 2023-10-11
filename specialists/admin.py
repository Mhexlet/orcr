from django.contrib import admin
from .models import Article, ArticleFile, ArticleApprovalApplication
from django.db.models.fields.reverse_related import ManyToOneRel


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Article._meta.get_fields() if type(field) != ManyToOneRel]


@admin.register(ArticleFile)
class ArticleFileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ArticleFile._meta.get_fields()]


@admin.register(ArticleApprovalApplication)
class ArticleApprovalApplicationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ArticleApprovalApplication._meta.get_fields()]