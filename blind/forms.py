from django import forms
from django.contrib.auth.forms import UserCreationForm
from blind.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label="username")
    password = forms.CharField(widget=forms.PasswordInput, label='password')

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return self.cleaned_data
            else:
                raise forms.ValidationError("Wrong password!")
        except User.DoesNotExist:
            raise forms.ValidationError("No user!")

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2",]

# class CardForm(forms.ModelForm):
#     class Meta:
#         model = Game
#         fields = ("attackcard",)   
