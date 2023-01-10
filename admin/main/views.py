from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib import messages , auth
from django.http import HttpResponse

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
