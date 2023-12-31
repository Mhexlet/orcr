# Generated by Django 4.2.5 on 2023-11-21 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_indexlink'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='place',
            options={'verbose_name': 'Город из географии ранней помощи', 'verbose_name_plural': 'Город из географии ранней помощи'},
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Название')),
                ('phone_number', models.CharField(max_length=16, verbose_name='Номер телефона')),
                ('address', models.TextField(verbose_name='Адрес')),
                ('link', models.TextField(verbose_name='Ссылка')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.place', verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Учреждение из географии ранней помощи',
                'verbose_name_plural': 'Учреждение из географии ранней помощи',
            },
        ),
    ]
