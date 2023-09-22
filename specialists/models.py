from django.db import models
from authentication.models import User


class Article(models.Model):

    STATUSES = (
        ('waiting', 'Ожидает проверки'),
        ('approved', 'Одобрено'),
        ('declined', 'Отклонено'),
    )

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Автор', related_name='articles')
    status = models.CharField(max_length=32, choices=STATUSES, verbose_name='Статус')
    hidden = models.BooleanField(default=False, verbose_name='Статья скрыта')
    theme = models.CharField(max_length=128, verbose_name='Тематика')
    title = models.CharField(max_length=128, verbose_name='Название статьи')
    text = models.TextField(verbose_name='Текст статьи')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата написания')
    approved_at = models.DateTimeField(null=True, verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title

    @property
    def get_files(self):
        return self.files.select_related()


class ArticleFile(models.Model):

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='documents/')

    class Meta:
        verbose_name = 'Файл из статьи'
        verbose_name_plural = 'Файлы из статей'
