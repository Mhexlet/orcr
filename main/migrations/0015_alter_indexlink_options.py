# Generated by Django 4.2.5 on 2023-11-24 16:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_alter_banner_options_alter_indexlink_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='indexlink',
            options={'verbose_name': 'Горячая ссылка', 'verbose_name_plural': 'Горячие ссылки'},
        ),
    ]
