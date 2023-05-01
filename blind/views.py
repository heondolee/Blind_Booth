from django.shortcuts import render
from re import template
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . import forms

def reservation(request):
    return render(request, "reservation.html")

class login_view(View):
    def get(self, request):
        form = forms.LoginForm()
        context = {
            "form": form,
        }
        return render(request, "reservation.html", context)
    
    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user=authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, "reservation.html")
        context = {
            "forms":form,
        }
        return render(request, "reservation.html", context=context)

@login_required(login_url='log_in')
def log_out(request):
    logout(request)
    return redirect("blind:reservation")

# def sign_up(request):
#     if request.method == "POST":
#         form = forms.SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return render(request, "reservation.html")
#         return redirect("blind:reservation")
#     else:
#         form = forms.SignupForm()
#         context = {
#             "form":form,
#         }
#         return render(request, "reservation.html", context=context)