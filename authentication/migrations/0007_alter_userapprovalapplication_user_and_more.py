# Generated by Django 4.2.5 on 2023-10-13 13:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userapprovalapplication',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approval_applications', to=settings.AUTH_USER_MODEL, verbose_name='Специалист'),
        ),
        migrations.CreateModel(
            name='UserEditApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.CharField(max_length=32, verbose_name='Поле')),
                ('old_value', models.TextField(verbose_name='Старое значение')),
                ('new_value', models.TextField(verbose_name='Новое значение')),
                ('time', models.DateTimeField(auto_now=True, verbose_name='Время создания')),
                ('treated', models.BooleanField(default=False, verbose_name='Обработана')),
                ('response', models.BooleanField(default=False, verbose_name='Вердикт')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='edit_applications', to=settings.AUTH_USER_MODEL, verbose_name='Специалист')),
            ],
        ),
    ]