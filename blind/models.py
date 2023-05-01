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
    phone_number = models.IntegerField()
    gender = models.IntegerField(choices=GenderChoices.choices)
    name = models.CharField(max_length=20)