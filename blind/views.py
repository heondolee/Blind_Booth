from django.shortcuts import render, redirect, HttpResponse
from re import template
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from blind.forms import PersonForm
from blind.models import User, Person, TimeBox, GenderChoices
import csv
from django.db.models import Q, Max
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib import messages
import requests

import hashlib
import hmac
import base64
import time
import os, sys
import django


def	make_signature():
    timestamp = str(int(time.time() * 1000))
    access_key = "m2ly34gJo3yRuuy2TS5y"
    secret_key = bytes('8H6SWmNYKXthJ6tWfO5WBNtJAt5wQrGhCvl0yRnz', 'UTF-8')
    method = "POST"
    message = method + " " + '/sms/v2/services/ncp:sms:kr:307397418568:blind_date/messages' + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signingKey



def send_sms(phone, mached_message):
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
        'content': mached_message,
        'messages': [{'to': phone}]
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
    times_7 = [12,13,14,15,16,17,18,19]
    context = {'fillteredTimeBoxs': fillteredTimeBoxs, 'menu_day':menu_day, 'menu_slot':menu_slot, 'times_7':times_7}
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
        
        if(time_box.man and time_box.woman):
            if(time_box.day == 1):
                matched_day = '5/9(화)'
            elif(time_box.day == 2):
                matched_day = '5/10수'
            else:
                matched_day = '5/11목'
            
            matched_slot = str(time_box.timeSlot)
            mached_min = time_box.timeMin
            mached_message = matched_day + matched_slot + ":" + mached_min

            matched_man = time_box.man
            matched_woman = time_box.woman

            mached_message = matched_day + matched_slot + ":" + mached_min
            post_message1 = "* 암흑 속 미팅 부스 *\n" + mached_message + "\n매칭성공" 
            post_message2 = "10000원 입금 후 입금자명을 알려주셔야 예약이 확정됩니다.\n100006770885 토스뱅크\n이*도"
            my_message = mached_message + "\n남: " + matched_man.phone_number + matched_man.name + "\n여: " + matched_woman.phone_number + matched_woman.name

            send_sms('01032495915', my_message)
            time.sleep(0.5)
            send_sms(matched_man.phone_number, post_message1)
            time.sleep(1)
            send_sms(matched_woman.phone_number, post_message1)
            time.sleep(1)
            send_sms(matched_man.phone_number, post_message2)
            time.sleep(1)
            send_sms(matched_woman.phone_number, post_message2)
            messages.warning(request, "입금 안내 문자가 발송되었습니다.")
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
            messages.warning(request, "매칭 신청이 완료되었습니다.")
    context = {'time_box': time_box, 'gender' : gender}
    return render(request, "detail.html", context=context)

def delay_message():
    pass



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


def dbToCsv(request):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django-erp2.settings")
    django.setup() 

    csv_path = '/home/ubuntu/Blind_Booth/static/csv/data.csv'

    with open(csv_path, 'w', newline='') as f_csv:
        field_names = ['day', 'timeSlot', 'timeMin', 'man_phone', 'woman_phone']
        data_writer = csv.DictWriter(f_csv, fieldnames=field_names) 
        data_writer.writeheader()

        # Delete the contents of the CSV file
        f_csv.truncate(0)
        for time_box in TimeBox.objects.all():
            if time_box.man == None:
                manPhone = "none"
            else:
                manPhone = time_box.man.phone_number
            if time_box.woman == None:
                womanPhone = "none"
            else:
                womanPhone = time_box.woman.phone_number
            data_writer.writerow({
                'day': time_box.day,
                'timeSlot': time_box.timeSlot, 
                'timeMin': time_box.timeMin, 
                'man_phone': manPhone, 
                'woman_phone': womanPhone, 
            })
                        
    return HttpResponse('create csv')

