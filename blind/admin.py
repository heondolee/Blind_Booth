from django.contrib import admin

# Register your models here.
from blind.models import User, Person


admin.site.register(User)
admin.site.register(Person)