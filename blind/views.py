from django.shortcuts import render, redirect
from re import template
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . import forms

def reservation(request):
    return render(request, "reservation.html")

@login_required(login_url='log_in')
def log_out(request):
    logout(request)
    return redirect("blind:reservation")
