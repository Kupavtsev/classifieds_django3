# Generated by Django 3.2.7 on 2022-09-15 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0004_remove_privatemessage_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='privatemessage',
            name='content',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='testapp.message'),
            preserve_default=False,
        ),
    ]