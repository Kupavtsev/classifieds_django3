# Generated by Django 3.2.7 on 2024-01-05 18:36

import bboard.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rubric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=20, verbose_name='Название')),
                ('show', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Рубрика',
                'verbose_name_plural': 'Рубрики',
                'ordering': ['name'],
            },
        ),
        migrations.AlterModelOptions(
            name='bb',
            options={'ordering': ['-published'], 'verbose_name': 'Объявление', 'verbose_name_plural': 'Объявления'},
        ),
        migrations.AddField(
            model_name='bb',
            name='changed',
            field=models.DateTimeField(auto_now=True, db_index=True, verbose_name='Изменено'),
        ),
        migrations.AddField(
            model_name='bb',
            name='kind',
            field=models.CharField(choices=[('Куплю', 'Куплю'), ('Продам', 'Продам'), ('Обменяю', 'Обменяю')], default=('Продам', 'Продам'), max_length=7),
        ),
        migrations.AddField(
            model_name='bb',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='bb',
            name='content',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='bb',
            name='price',
            field=models.FloatField(blank=True, null=True, validators=[bboard.models.validate_even], verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='bb',
            name='published',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано'),
        ),
        migrations.AlterField(
            model_name='bb',
            name='title',
            field=models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(bboard.models.get_min_length)], verbose_name='Товар'),
        ),
        migrations.AlterUniqueTogether(
            name='bb',
            unique_together={('title', 'price')},
        ),
        migrations.AddField(
            model_name='bb',
            name='rubric',
            field=models.ForeignKey(limit_choices_to={'show': True}, null=True, on_delete=django.db.models.deletion.PROTECT, to='bboard.rubric', verbose_name='Рубрика'),
        ),
    ]
