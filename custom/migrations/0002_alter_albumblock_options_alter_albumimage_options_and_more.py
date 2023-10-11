# Generated by Django 4.2.5 on 2023-09-28 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='albumblock',
            options={'verbose_name': 'Альбом', 'verbose_name_plural': 'Альбомы'},
        ),
        migrations.AlterModelOptions(
            name='albumimage',
            options={'verbose_name': 'Изображение из альбома', 'verbose_name_plural': 'Изображения из альбомов'},
        ),
        migrations.AlterModelOptions(
            name='filesetblock',
            options={'verbose_name': 'Набор файлов', 'verbose_name_plural': 'Наборы файлов'},
        ),
        migrations.AlterModelOptions(
            name='filesetfile',
            options={'verbose_name': 'Файл из набора', 'verbose_name_plural': 'Файлы из наборов'},
        ),
        migrations.AlterModelOptions(
            name='page',
            options={'verbose_name': 'Страница', 'verbose_name_plural': 'Страницы'},
        ),
        migrations.AlterModelOptions(
            name='section',
            options={'verbose_name': 'Раздел', 'verbose_name_plural': 'Разделы'},
        ),
    ]