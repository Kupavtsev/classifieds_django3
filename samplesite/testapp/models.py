from django.db import models
from django.contrib.auth.models import User
import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# from django.contrib.postgres.constraints import ExclusionConstraint
# from django.contrib.postgres.indexes import GistIndex
# from django.contrib.postgres.fields import (DateTimeRangeField, ArrayField, HStoreField,
#                                             CICharField, JSONField, RangeOperators)


#           ========================================= 
#           ---===         1 OneToOne          ===---
#           ========================================= 
class AdvUser(models.Model):
    is_activated = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Активированные'
        verbose_name        = 'Активированный'
        ordering            = ['is_activated']


#           ========================================= 
# 2 Choices
#           ========================================= 
class Mesure(models.Model):
    class Mesurments(float, models.Choices):
        METERS = 1.0, 'Метры'
        FEETS = 0.3048, 'Футы'
        YARDS = 0.9144, 'Ярды'

    mesurment = models.FloatField(choices=Mesurments.choices)


#           ========================================= 
#           ---===        3 ManyToMany         ===---
#           ========================================= 
class Spare(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Machine(models.Model):
    name = models.CharField(max_length=30)
    spares = models.ManyToManyField(Spare)
    # spares = models.ManyToManyField(Spare, through='Kit', through_fields=('machine', 'spare'))

# https://stackoverflow.com/questions/26927705/django-migration-error-you-cannot-alter-to-or-from-m2m-fields-or-add-or-remove
# class Kit(models.Model):
#     machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
#     spare = models.ForeignKey(Spare, on_delete=models.CASCADE)
#     count = models.IntegerField()

class TestID(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=10)

#           ========================================= 
#           ---===        4 Notes              ===---
#           ========================================= 
class Note(models.Model):
    content = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')

    class Meta:
        permissions = (('hide_notes', 'Можно скрыть заметки'),)


#           ========================================= 
#           ---===        5 Messages           ===---
#           ========================================= 

# 5.1
class Message(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content

class PrivateMessage(Message):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.OneToOneField(Message, on_delete=models.CASCADE,
                                    parent_link=True)


# 5.1
# This is Abstract, so it doesnot create tables in DB
# class Message(models.Model):
#     content = models.TextField()
#     name = models.CharField(max_length=20)
#     email = models.EmailField()

#     class Meta:
#         abstract = True
#         ordering = ['name']

# class PrivateMessage(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     # Переопределяем поле name
#     name = models.CharField(max_length=40)
#     # Удаляем поле email
#     email = None

#     class Meta(Message.Meta):
#         pass



#               It  would not work with SQLite!!!
#           ========================================= 
#           ---===        6 PostgreSQL 18      ===---
#           =========================================
# class PGSRoomServing(models.Model):
#     name = models.CharField(max_length=20, verbose_name='Помещение')
#     reserving = DateTimeRangeField(verbose_name='Время резервирования')
#     cancelled = models.BooleanField(default=False, verbose_name='Отменить резервирования')

#     class Meta:
#         indexes = [
#             GistIndex(fields=['reserving'], name='i_pgsrr_reserving',
#                         opclasses=('range_ops',), fillfactor=50)
#         ]
#         constraints = [
#             ExclusionConstraint(name='c_pgsrr_reserving',
#                                 expressions=[('name', RangeOperators.EQUAL),
#                                 ('reserving', RangeOperators.OVERLAPS)],
#                                 condition=models.Q(cancelled=False))
#         ]


# class PGSRubric(models.Model):
#     name = models.CharField(max_length=20, verbose_name='Имя')
#     description = models.TextField(verbose_name='Описание')
#     tags = ArrayField(base_field=models.CharField(max_length=20), default=list, verbose_name='Теги')

#     class Meta:
#         indexes = [
#             models.Index(fields=('name', 'description'),
#                                 name='i_pgsrubric_name_description',
#                                 opclasses=('varchar_pattern_ops', 'bpchar_pattern_ops'))
#         ]

#         constraints = [
#             ExclusionConstraint(name='c_pgsrubric_name_description',
#                                 expressions=[('name', RangeOperators.EQUAL),
#                                 ('description', RangeOperators.EQUAL)])
#             ]

# class PGSProject(models.Model):
#     name = models.CharField(max_length=40, verbose_name='Название')
#     platforms = ArrayField(base_field=ArrayField(models.CharField(max_length=20), default=list), default=list, verbose_name='Использованные платформы')

# class PGSProject2(models.Model):
#     name = models.CharField(max_length=40, verbose_name='Название')
#     platforms =HStoreField(verbose_name='Использованные платформы')

# class PGSProject3(models.Model):
#     name = CICharField(max_length=40, verbose_name='Название')
#     data = JSONField()