# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.urls import reverse

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from models import *

# Create your views here.


def checkAuth(request):
    try:
        m = request.session['member_id']
    except:
        return 0
    return m


def index(request):
    logged_in = checkAuth(request)
    return render(request, "index.html", context={'log': logged_in})


def dashboard(request):
    logged_in = checkAuth(request)
    return render(request, "dashboard.html", context={'log': logged_in})


def form(request):
    return render(request, 'form.html')


def studentlogin(request):
    name = request.POST['email']
    pwd = request.POST['password']
    context = {}
    try:
        usr = Student.objects.get(email=name)
    except (KeyError, Student.DoesNotExist):
        context['errors'] = True
        return render(request, "form.html", context)
    else:
        if (usr.password == pwd):
            if usr.type != "Student":
                return HttpResponseRedirect(reverse('teachersupport:form'))
            else:
                usr.logged_in = True
                usr.save()
                request.session['member_id'] = usr.id
                request.session['logged_type'] = usr.type
                profs = []
                professors = Professor.objects.all()
                for i in range(0, len(professors)):
                    profs.append(professors[i].name)
                request.session['professors'] = profs

                request.session.set_expiry(0)
                return HttpResponseRedirect(reverse('teachersupport:dashboard'))
        else:
            return render(request, "form.html", context)


def proflogin(request):
    name = request.POST['email']
    pwd = request.POST['password']
    context = {}
    try:
        usr = Professor.objects.get(email=name)
    except (KeyError, Professor.DoesNotExist):
        context['errors'] = True
        return render(request, "form.html", context)
    else:
        if (usr.password == pwd):
            if usr.type != "Professor":
                return render(request, "form.html", context)
            else:
                usr.logged_in = True
                usr.save()
                officehourrequests = OfficeHours.objects.all()
                students = {}
                all_students = Student.objects.all()
                for i in range(0, len(all_students)):
                    students[all_students[i].id] = all_students[i].id
                request.session['students'] = students
                requests = {}
                requests[usr.id] = []
                for i in officehourrequests:
                    if i.professor.id == usr.id:
                        requests[usr.id].append(i.student_id)

                students_in_need = []
                for i in requests:
                    for j in requests[i]:
                        std_obj_id = Student.objects.get(id=j).id
                        std_obj_name = Student.objects.get(id=j).name
                        std_request = {}
                        std_request[std_obj_id] = std_obj_name
                        if any(std_obj_id in d for d in students_in_need) == False:
                            students_in_need.append((std_obj_id, std_obj_name))
                        else:
                            pass
                request.session['member_id'] = usr.id
                request.session['logged_type'] = usr.type
                request.session['officehour_requests'] = requests
                request.session['students_in_need'] = students_in_need
                request.session.set_expiry(0)
                return HttpResponseRedirect(reverse('teachersupport:dashboard'))
        else:
            return render(request, "form.html", context)


def logout(request):
    if request.session['member_id'] == '':
        return render(request, "form.html", context)
    else:

        try:
            m_id = request.session['member_id']
        except KeyError:
            pass
        else:
            m = Student.objects.get(pk=m_id) or Professor.objects.get(pk=m_id)
            m.logged_in = False
            m.save()
            del request.session['member_id']
            return render(request, "index.html")


def requestofficehours(request):
    student_id = request.POST.get('student', '')
    professor_needed = request.POST.get('professor', '')
    student_name = Student.objects.get(id=student_id).name
    try:
        usr = Professor.objects.get(name=professor_needed)
        usr_id = usr.id
    except (KeyError, Professor.DoesNotExist):
        context['errors'] = True
        return render(request, "dashboard.html", context)
    else:
        officeHour = OfficeHours.objects.create(
            student_id=student_id, professor_needed=professor_needed, professor=usr
        )
        return HttpResponseRedirect(reverse('teachersupport:dashboard'))


def signup(request):
    name = request.POST.get('name', '')
    mail = request.POST.get('email', '')
    password = request.POST.get('passwordsignup', '')
    pwd2 = request.POST.get('passwordsignup_confirm', '')
    accountType = request.POST.get('account_type', '')
    context = {}

    if (password != pwd2):
        context['wrong'] = True
        return render(request, "form.html", context)
    else:
        if accountType == 'Student':
            studentMember = Student.objects.create(
                name=name, email=mail, password=password, logged_in=True)
        else:
            profMember = Professor.objects.create(
                name=name, email=mail, password=password, available_time=time_available, logged_in=True
            )

        return HttpResponseRedirect(reverse('teachersupport:index'))

    return HttpResponse("signup")
