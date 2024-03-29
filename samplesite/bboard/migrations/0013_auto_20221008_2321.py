# Generated by Django 3.2.7 on 2022-10-08 20:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bboard', '0012_alter_bb_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='bb',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='bb',
            name='kind',
            field=models.CharField(choices=[('Куплю', 'Куплю'), ('Продам', 'Продам'), ('Обменяю', 'Обменяю')], default=('Продам', 'Продам'), max_length=7),
        ),
    ]
