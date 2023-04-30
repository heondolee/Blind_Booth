from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser,models.Model):
    totalscore = models.IntegerField(default=0,verbose_name="totalscore")