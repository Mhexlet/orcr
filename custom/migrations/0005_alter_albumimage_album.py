# Generated by Django 4.2.5 on 2023-10-30 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('custom', '0004_alter_albumimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='albumimage',
            name='album',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='custom.albumblock', verbose_name='Альбом'),
        ),
    ]
