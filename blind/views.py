from django.shortcuts import render, redirect, HttpResponse
from re import template
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from blind.forms import PersonForm
from blind.models import User, Person, TimeBox
import csv




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
            print(person.name)
            return redirect("blind:reservation")
    else:
        form = PersonForm(instance=person)
    return render(request, 'info_update.html', {'form': form})

def csvToModel(request):
    TimeBox.objects.all().delete()

    a = open("./static/csv/timezone.csv",'r',encoding='CP949')
    
    reader_timezone = csv.reader(a)

    timeBoxes= []

    for row in reader_timezone:
        timeBoxes.append(TimeBox(day=row[0],timeSlot=row[1],timeMin=row[2]))
    
    TimeBox.objects.bulk_create(timeBoxes)

    a.close()

    return HttpResponse('create model~')
