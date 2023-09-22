import os
from django.db import models


class Section(models.Model):

    name = models.CharField(max_length=64, verbose_name='Название раздела')

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def __str__(self):
        return self.name

    @property
    def get_pages(self):
        return self.pages.select_related()


class Page(models.Model):

    title = models.CharField(max_length=32, unique=True, verbose_name='Заголовок страницы')
    url = models.CharField(max_length=16, unique=True, verbose_name='URL страницы (перевод заголовка на английский, в нижнем регистре, с _ вместо пробелов)')
    section = models.ForeignKey(Section, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Раздел меню (оставьте незаполненным, если страница не является подразделом)', related_name='pages')
    content = models.TextField(verbose_name='Содержимое')
    approved = models.BooleanField(default=False, verbose_name='Публичный доступ')

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'

    def __str__(self):
        return self.title


# class PageBlock(models.Model):
#
#     TYPES = (
#         ('text', 'Текст'),
#         ('image', 'Изображение'),
#         ('map', 'Карта'),
#         ('html', 'HTML код'),
#         ('album', 'Альбом'),
#         ('file_set', 'Набор файлов'),
#     )
#
#     page = models.ForeignKey(Page, on_delete=models.CASCADE, verbose_name='Страница')
#     order = models.SmallIntegerField(verbose_name='Порядковый номер блока на странице')
#     type = models.CharField(max_length=32, choices=TYPES, verbose_name='Тип блока')


# class TextBlock(PageBlock):
#
#     text = models.TextField(verbose_name='Текст')
#
#
# class ImageBlock(PageBlock):
#
#     image = models.ImageField(upload_to='images/', verbose_name='Изображение')
#     name = models.CharField(max_length=128, null=True, blank=True, verbose_name='Подпись (необязательно)')
#
#
# class MapBlock(PageBlock):
#
#     src = models.TextField(verbose_name='Ссылка на карту')
#     name = models.CharField(max_length=128, null=True, blank=True, verbose_name='Подпись (необязательно)')


# class HTMLBlock(PageBlock):
#
#     html = models.TextField(verbose_name='HTML код')


class AlbumBlock(models.Model):

    page = models.ForeignKey(Page, on_delete=models.CASCADE, verbose_name='Страница')
    name = models.CharField(max_length=64, null=True, verbose_name='Название')

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'

    @property
    def get_images(self):
        return self.images.select_related()

    def __str__(self):
        return self.name


class FileSetBlock(models.Model):

    page = models.ForeignKey(Page, on_delete=models.CASCADE, verbose_name='Страница')
    name = models.CharField(max_length=64, null=True, verbose_name='Название')

    class Meta:
        verbose_name = 'Набор файлов'
        verbose_name_plural = 'Наборы файлов'

    @property
    def get_files(self):
        return self.files.select_related()

    def __str__(self):
        return self.name


class AlbumImage(models.Model):

    image = models.ImageField(upload_to='images/', verbose_name='Изображение')
    album = models.ForeignKey(AlbumBlock, on_delete=models.SET_NULL, null=True, related_name='images', verbose_name='Альбом')
    name = models.CharField(max_length=128, null=True, blank=True, verbose_name='Название (необязательно)')

    class Meta:
        verbose_name = 'Изображение из альбома'
        verbose_name_plural = 'Изображения из альбомов'

    def __str__(self):
        return self.image.name


class FileSetFile(models.Model):

    file = models.FileField(upload_to='documents/', verbose_name='Файл')
    file_set = models.ForeignKey(FileSetBlock, on_delete=models.SET_NULL, null=True, related_name='files', verbose_name='Набор файлов')
    name = models.CharField(max_length=128, null=True, blank=True, verbose_name='Название (необязательно)')

    class Meta:
        verbose_name = 'Файл из набора'
        verbose_name_plural = 'Файлы из наборов'

    def __str__(self):
        return self.file.name

    @property
    def extension(self):
        name, ext = os.path.splitext(self.file.name)
        return ext
