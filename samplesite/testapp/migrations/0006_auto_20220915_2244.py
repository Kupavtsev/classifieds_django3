# Generated by Django 3.2.7 on 2022-09-15 19:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0005_privatemessage_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='privatemessage',
            name='content',
        ),
        migrations.RemoveField(
            model_name='privatemessage',
            name='id',
        ),
        migrations.AddField(
            model_name='privatemessage',
            name='message',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='testapp.message'),
            preserve_default=False,
        ),
    ]