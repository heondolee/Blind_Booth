from django.shortcuts import render
from re import template
from django.shortcuts import redirect

def reservation(request):
    return render(request, 'reservation.html')

