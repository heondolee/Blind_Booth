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
from django.contrib import messages
import requests

import time
import hashlib
import hmac
import base64


def	make_signature():
    timestamp = str(int(time.time() * 1000))
    access_key = "m2ly34gJo3yRuuy2TS5y"
    secret_key = bytes('8H6SWmNYKXthJ6tWfO5WBNtJAt5wQrGhCvl0yRnz', 'UTF-8')
    method = "POST"
    message = method + " " + '/sms/v2/services/ncp:sms:kr:307397418568:blind_date/messages' + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signingKey



def send_sms():
    timestamp = str(int(time.time() * 1000))

    url = 'https://sens.apigw.ntruss.com/sms/v2/services/ncp:sms:kr:307397418568:blind_date/messages'
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': 'm2ly34gJo3yRuuy2TS5y',
        'x-ncp-apigw-signature-v2': make_signature()
    }
    data = {
        'type': 'SMS',
        'from': "01032495915",
        'content': "통신보안 들이나 다진?",
        'messages': [{'to': "01047314189"}]
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    return result




def reservation(request):
    # send_sms()
    if request.method == 'POST': #로그인, person, 예약 보장됨
        time_box_id = request.POST.get('cancel_time_box_id')
        time_box = TimeBox.objects.get(id=time_box_id)

        current_user = request.user
        person = current_user.person_set.get()

        if(person.gender == 1):
            time_box.man = None
            time_box.save()
        else:
            time_box.woman = None
            time_box.save()

        messages.warning(request, "신청이 취소되었습니다.")
    else:
        pass
    try:
        current_user = request.user
        person = current_user.person_set.get()
        if (person.gender == 1):
            time_boxs = TimeBox.objects.filter(man=person)
        else:
            time_boxs = TimeBox.objects.filter(woman=person)
    except:
        time_boxs = 0
        person = 0
    context = {'time_boxs': time_boxs, 'person': person,}

    return render(request, "reservation.html", context)

def timebox_detail(request):
    person = request.user.person_set.first()
    man_timeboxes = TimeBox.objects.filter(man=person)
    woman_timeboxes = TimeBox.objects.filter(woman=person)
    context = {'man_timeboxes': man_timeboxes, 'woman_timeboxes': woman_timeboxes}
    return render(request, 'timebox_detail.html', context)

def reserve_page(request,day,slot):
    if request.method == 'POST':
        menu_day = request.POST.get('day')
        menu_slot = request.POST.get('timeSlot')
        return redirect(f"/reserve_page/{menu_day}/{menu_slot}")
    else:
        menu_day = day
        menu_slot = slot
    fillteredTimeBoxs = list(TimeBox.objects.filter(Q(day=menu_day)&Q(timeSlot=menu_slot)))
    context = {'fillteredTimeBoxs': fillteredTimeBoxs, 'menu_day':menu_day, 'menu_slot':menu_slot}
    return render(request, "reserve_page.html", context=context)


@login_required
def detail(request, id, gender):
    time_box = TimeBox.objects.get(id=id)
    if request.method == 'POST':
        current_user = request.user
        person = current_user.person_set.get()
        if(gender == 1):
            time_box.man = person
            time_box.save()
        elif(gender == 2):
            time_box.woman = person
            time_box.save()
        
        # if(time_box.man and time_box.woman):
        #     matched_man = time_box.man_timebox_set.get()
        #     matched_woman = time_box.woman_timebox_set.get()
        #     man_phone = matched_man.phone_number
        #     woman_phone = matched_woman.phone_number
        #     send_sms(man_phone, woman_phone)
        return redirect(f"/detail/{id}/{gender}")
    else:
        try:
            person = request.user.person_set.get()
        except Person.DoesNotExist:
            messages.warning(request, "전화번호를 등록하세요")
            return render(request, "reservation.html")
            # 
        # -> try 정상작동
        if(person.gender!=gender):
            messages.warning(request, "성별이 다릅니다.")
            return redirect(f"/reserve_page/{time_box.day}/{time_box.timeSlot}")
        else:
            pass
    context = {'time_box': time_box, 'gender' : gender}
    return render(request, "detail.html", context=context)



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
        timeBoxes.append(TimeBox(day=row[0],timeSlot=row[1],timeMin=row[2], id=row[0] + row[1] + row[2]))
    
    TimeBox.objects.bulk_create(timeBoxes)

    a.close()

    return HttpResponse('create model~')
