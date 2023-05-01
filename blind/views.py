from django.shortcuts import render, redirect
from re import template
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from blind.forms import PersonForm
from blind.models import User, Person



def reservation(request):
    return render(request, "reservation.html")

@login_required(login_url='log_in')
def log_out(request):
    logout(request)
    return redirect("blind:reservation")

@login_required(login_url='log_in')
def info_update(request):
    current_user = request.user
    try:
        person = current_user.person_set.get()
    except Person.DoesNotExist:
        person = None
    
    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            person = form.save(commit=False)
            person.user = current_user
            person.save()
            print(person.phone_number)
            print(person.gender)
            print(person.user.username)
            return redirect("blind:reservation")
    else:
        form = PersonForm(instance=person)
    return render(request, 'info_update.html', {'form': form})

