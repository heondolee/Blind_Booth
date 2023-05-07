from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Person, GenderChoices

class PersonForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=GenderChoices.choices)

    class Meta:
        model = Person
        fields = ('phone_number', 'gender')