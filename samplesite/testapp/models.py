from django.db import models
from django.contrib.auth.models import User
import uuid

# OneToOne
class AdvUser(models.Model):
    is_activated = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Активированные'
        verbose_name        = 'Активированный'
        ordering            = ['is_activated']

# Choices
class Mesure(models.Model):
    class Mesurments(float, models.Choices):
        METERS = 1.0, 'Метры'
        FEETS = 0.3048, 'Футы'
        YARDS = 0.9144, 'Ярды'

    mesurment = models.FloatField(choices=Mesurments.choices)

# ManyToMany
class Spare(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Machine(models.Model):
    name = models.CharField(max_length=30)
    spares = models.ManyToManyField(Spare)

class TestID(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=10)