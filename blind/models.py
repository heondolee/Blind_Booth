from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class GenderChoices(models.IntegerChoices):
    MALE = 1, '남자'
    FEMALE = 2, '여자'

class Person(models.Model):
    user = models.ForeignKey(
        User, 
        related_name='person_set', 
        on_delete=models.CASCADE
    )
    phone_number = models.CharField(max_length=11)
    gender = models.IntegerField(choices=GenderChoices.choices)
    name = models.CharField(max_length=20)

class TimeBox(models.Model):
    man = models.ForeignKey(
        Person,
        related_name='man_timebox_set',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    woman = models.ForeignKey(
        Person,
        related_name='woman_timebox_set',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    day = models.IntegerField()
    timeSlot = models.IntegerField()
    timeMin = models.CharField(max_length=2)
    manIn = models.BooleanField(default=False)
    womanIn = models.BooleanField(default=False)