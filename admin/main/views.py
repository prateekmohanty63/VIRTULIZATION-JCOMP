
from collections import UserList
from os import stat_result
from pickle import NONE
from pydoc import Doc
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages

from main.models import Hospital, Doctor, DocReview, DocAppointment, HospitalReview
from .forms import DoctorForm, HospitalForm
from django import forms
from .choices import Department, States
from django.contrib import auth
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail

# Create your views here.


def index(request):

    return render(request,'index.html')


def userRegistration(request):

    if request.method == "POST":
       # userform = UserForm(request.POST, request.FILES)
        print("POST")
        firstName = request.POST['fname']
        lastName = request.POST['lname']
        email = request.POST['email']
        dateOfBirth = request.POST['date']
        userName = request.POST['user_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        mobileNo = request.POST['mobileNumber']

        print(password1)
        print(password2)

        if password1 == password2:
            print("in")
            if User.objects.filter(username=userName).exists():
                messages.info(request, 'username taken')
                return redirect('userReg')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email is taken')
                return redirect('userReg')
            else:

                print('form is valid')
                user = User.objects.create_user(
                    username=userName, password=password1, email=email)
                # user.is_active = False
                user.save()
            # Save the Data to the Database
                # userform.save()
                return HttpResponse("REGISTERED")

               

        else:
            messages.info(request, "Password not matching")
            return redirect('userRegistration')

    if request.method == "GET":
        print("GET")
        return render(request, "user_registration.html")




def doctorRegistration(request):

    if request.method == "POST":
        # creating an instance of the Doctor registration form
        doctorForm = DoctorForm(request.POST, request.FILES)

        # print(doctorForm)

        username = request.POST['Username']
        password = request.POST['psw']
        email = request.POST['Email']
        print(username, password, email)

        emailerror = ""
        usernameerror = ""

        if User.objects.filter(username=username).exists():
            usernameerror = "Username already exists"
        else:
            usernameerror = ""

        if User.objects.filter(email=email).exists():
            emailerror = "email already exists"
        else:
            emailerror = ""

        context = {
            "form": DoctorForm,
            "emailerror": emailerror,
            "usernameerror": usernameerror
        }

        # if there is an error
        if usernameerror != "" or emailerror != "":
            print("in")
            return render(request, 'doctor_regestration.html', context)

        if doctorForm.is_valid():
            print(username)
            user = User.objects.create_user(
                username=username, password=password, email=email)
            user.save()

            doctorForm.save()
            return HttpResponse("Registered")

    else:
        form = DoctorForm()
        context = {'form': form}

        return render(request, 'doctor_regestration.html', context)




def signUp(request):
    return render(request, 'signup.html')


def signout(request):
    user = request.user
    context = {
        'USER': user
    }
    auth.logout(request)
    messages.success(request, "Signed out successfully", context)
    return redirect('index')


def signIn(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)

        # based on returned value user get logged .
        if user is not None:
            auth.login(request, user)
            messages.success(request, "Signed in successfully")
            return redirect('index')
        else:
            return render(request, 'signin_fail.html')
    else:
        return render(request, 'signin.html')
