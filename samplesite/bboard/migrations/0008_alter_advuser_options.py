# Generated by Django 3.2.7 on 2022-02-16 17:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0007_advuser'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='advuser',
            options={'ordering': ['is_activated'], 'verbose_name': 'Активированный', 'verbose_name_plural': 'Активированные'},
        ),
    ]