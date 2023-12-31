# Generated by Django 4.2.5 on 2023-10-25 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_sitecontent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='tmp/', verbose_name='Изображение')),
                ('name', models.CharField(max_length=128, verbose_name='Название')),
                ('link', models.TextField(verbose_name='Ссылка')),
            ],
            options={
                'verbose_name': 'Баннер-ссылка',
                'verbose_name_plural': 'Баннеры-ссылки',
            },
        ),
        migrations.AlterField(
            model_name='mainsliderimage',
            name='image',
            field=models.ImageField(upload_to='tmp/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.ImageField(upload_to='tmp/', verbose_name='Изображение'),
        ),
    ]
