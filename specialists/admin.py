from django.contrib import admin
from .models import Article, ArticleFile


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Article._meta.get_fields()]


@admin.register(ArticleFile)
class ArticleFileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ArticleFile._meta.get_fields()]