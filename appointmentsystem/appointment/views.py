
from collections import UserList
from os import stat_result
from pickle import NONE
from pydoc import Doc
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Hospital, Doctor, DocReview, DocAppointment, HospitalReview
from .forms import DoctorForm, HospitalForm
from django import forms
from .choices import Department, States
from django.contrib import auth
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from rest_framework import viewsets
from rest_framework import viewsets,status
from .serializers import AppointmentSerializers
from rest_framework.response import Response

# Create your views here.


def index(request):
    return HttpResponse('Appointment Service')
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


def hospitalRegistration(request):

    if request.method == "POST":
        hospitalform = HospitalForm(request.POST, request.FILES)

        username = request.POST['Username']
        password = request.POST['psw']
        confirmPassword = request.POST['cpsw']
        email = request.POST['Email']
        hospitalReg = request.POST.get('HospitalRegistrationNumber', '123')

        print(username, password, email, hospitalReg)

        usernameerror = ""
        emailerror = ""
        regerror = ""
        passworderror = ""

        # checking if the username already exists
        if User.objects.filter(username=username).exists():
            usernameerror = "email id already exists"
        else:
            usernameerror = ""

        # checking if the email already exists
        if User.objects.filter(email=email).exists():
            emailerror = "Email already exists"
        else:
            emailerror = ""

        # checking hospital registration number already exists
        print("before")
        if Hospital.objects.filter(HospitalRegisterationNumber=hospitalReg).exists():
            regerror = "Hospital with the registraiton number already exists"
        else:
            regerror = ""

        if password != confirmPassword:
            passworderror = "Passwords not matching"
        else:
            passworderror = ""

        print("after")

        context = {
            "form": HospitalForm,
            "usernameerror": usernameerror,
            " emailerror": emailerror,
            " regerror": regerror,
            " passworderror": passworderror
        }

        if usernameerror != "" or emailerror != "" or regerror != "" or passworderror != "":
            return render(request, 'Hospitalregistion.html', context)

        if hospitalform.is_valid():
            user = User.objects.create_user(
                username=username, password=password, email=email)
            user.save()

            hospitalform.save()

            return HttpResponse("Hospital registered")

    if request.method == "GET":
        hospitalform = HospitalForm()
        context = {'form': hospitalform}
        return render(request, 'Hospitalregistion.html', context)






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




# doctor appointment

def DoctorAppointment(request):

    if request.method == "POST":
        DoctorUsername = request.POST['dname']
        DateOfAppointment = request.POST['date']
        additionalMessage = request.POST['message']

        # Checking weather the user is signed in or not
        if not request.user.is_authenticated:
            messages.error(request, "Please sign in ")
            return redirect('index')

        # retriving the user and doctor
        user = User.objects.all().filter(username=request.user.username).get()
        doctor = Doctor.objects.all().filter(Username=DoctorUsername).get()
        # print(user)

        # checking weather the doctor exists or not
        if not doctor:
            messages.error(request, 'Doctor does not exists')
            return redirect('index')

        appointment = DocAppointment(
            user=user, doctor=doctor, dateOfAppointment=DateOfAppointment, AdditionalMessage=additionalMessage)
        appointment.save()


        userSubject = "Reference for your appointment"
        userBody = ("Hi " + user.username + 
                    "\n\nHere is what we got from you" + 
                    "\n\nDoctor Name: " + doctor.FirstName + doctor.LastName + 
                    "\n\nAppointment Date: " + DateOfAppointment + 
                    "\n\nAdditional Message: " + additionalMessage + 
                    "\n\nThe doctor will message to your appointment enquiry to your email in a span of 2-3 days" + 
                    "\n\nFor any queries please reply to this mail"
                )
        userEmail = request.user.email

        useremail = send_mail (
                userSubject,
                userBody,
                "prateekmohanty63@gmail.com",
                ["prateekmohanty63@gmail.com"],
                fail_silently=False
        )

        doctorSubject = "Appointment enquiry from " + user.username 
        doctorBody = ("Hi Doctor " + doctor.FirstName + doctor.LastName + 
                    "\n\nThis is to inform you that we got an appointment request from " + user.username+ 
                    "\n\nAppointment Date: " + DateOfAppointment + 
                    "\n\nAdditional Message: " + additionalMessage + 
                    "\n\nPlease respond to his enquiry within 2-3 days, and contact with the user if necessary" + 
                    "\n\nFor any queries please reply to this mail"
                )

        doctorEmail = doctor.Email

        doctoremail= send_mail (
                doctorSubject,
                doctorBody,
                "prateekmohanty63@gmail.com",
                [doctorEmail],
                fail_silently=False
        )

        # send a mail to doctor and the user

        messages.success(request, 'Appointment sent successfully')
        return redirect('index')






# appointment crud

class AppointmentViewSet(viewsets.ViewSet):
    def list(self,request):
        pass  #/main/appointments

    def create(self,request):
        serializer=AppointmentSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)