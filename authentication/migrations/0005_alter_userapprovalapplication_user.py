# Generated by Django 4.2.5 on 2023-10-09 13:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_user_approved_userapprovalapplication'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userapprovalapplication',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to=settings.AUTH_USER_MODEL, verbose_name='Специалист'),
        ),
    ]
