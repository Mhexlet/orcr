# Generated by Django 4.2.5 on 2024-01-09 12:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0015_user_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profession',
            field=models.CharField(max_length=64, verbose_name='Специализация'),
        ),
        migrations.CreateModel(
            name='FoAUserConnection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.fieldofactivity', verbose_name='Сфера деятельности')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Сфера деятельности пользователей',
                'verbose_name_plural': 'Сферы деятельности пользователей',
            },
        ),
    ]