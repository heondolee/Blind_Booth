from django.shortcuts import render, redirect, HttpResponse
from re import template
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from blind.forms import PersonForm
from blind.models import User, Person, TimeBox
import csv
from django.db.models import Q, Max
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

def reservation(request):
    return render(request, "reservation.html")

def reserve_page(request,day,slot):
    if request.method == 'POST':
        menu_day = request.POST.get('day')
        menu_slot = request.POST.get('timeSlot')
        return redirect(f"/reserve_page/{menu_day}/{menu_slot}")
    else:
        menu_day = day
        menu_slot = slot
    print(menu_day,menu_slot)
    fillteredTimeBoxs = list(TimeBox.objects.filter(Q(day=menu_day)&Q(timeSlot=menu_slot)))
    print(fillteredTimeBoxs)
    context = {'fillteredTimeBoxs': fillteredTimeBoxs, 'menu_day':menu_day, 'menu_slot':menu_slot}
    return render(request, "reserve_page.html", context=context)


def detail(request):
    if request.method == 'POST':
        day = request.POST.get('day')
        timeSlot = request.POST.get('timeSlot')
    else:
        day = 1
        timeSlot = 12
    
    fillteredTimeBoxs = list(TimeBox.objects.filter(Q(day=day)&Q(timeSlot=timeSlot)))
    context = {'fillteredTimeBoxs': fillteredTimeBoxs }
    return render(request, "reservation.html", context=context) 


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

@csrf_exempt
def days(request):
    req = json.loads(request.body)
    day = req[day] # 1->화 2-> 수 3->목
    return JsonResponse({ day : day})