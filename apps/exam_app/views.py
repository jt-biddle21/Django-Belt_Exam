from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from time import gmtime, strftime


def index(request):
    return render(request, 'exam_app/index.html')


def register(request):
    response = User.objects.basic_validator(request.POST, "Register")
    if type(response) == list:
        for error in response:
            messages.error(request, error)
        return redirect('/')
    request.session['user_id'] = response.id
    messages.success(request, "Registration Complete!")
    return redirect('/')


def login(request):
    response = User.objects.basic_validator(request.POST, "Login")
    if type(response) == list:
        for lerror in response:
            messages.error(request, lerror)
        return redirect('/')
    request.session['user_id'] = response.id
    messages.success(request, "Logged In!")
    return redirect('/loggedin')


def add(request, number):
    t = NewTask.objects.create(newtaskname=request.POST['addtask'], newtasktime=request.POST['addTime'], newtaskdate=request.POST['addDate'])
    t.save()
    User.objects.get(id=number).newtasks.add(t)
    return redirect('/loggedin')


def loggedin(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    context = {
        "task": User.objects.get(id=request.session['user_id']).tasks.all(),
        "newappoint": User.objects.get(id=request.session['user_id']).newtasks.all(),
        'username': User.objects.filter(id=request.session['user_id']),
        "time": strftime("%A %d, %Y", gmtime()),
    }
    return render(request, 'exam_app/loginshow.html', context)


def abouttoedit(request, number):
    editcontext = {
        "editappointment": Task.objects.filter(id=number),
    }
    return render(request, 'exam_app/updateappointment.html', editcontext)


def edit(request, number): #Not quite sure why this doesnt work
    taskedit = Task.objects.get(id=number) #im grabbing the appointment and setting the new status, name, date, and time. But it wont update
    taskedit.taskname = request.POST['newtask']
    taskedit.taskstatus = request.POST['newstatus']
    taskedit.taskdate = request.POST['newdate']
    taskedit.tasktime = request.POST['newtime']
    taskedit.save() #even after i saved it
    return redirect('/loggedin')


def delete(request, number):
    Task.objects.filter(id=number).delete()
    return redirect('/loggedin')


def logout(request):
    del request.session['user_id']

    return redirect('/')
