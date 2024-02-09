from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from .models import RegisterDB
from django.shortcuts import render, redirect
from django.contrib import messages

from django.core.mail import send_mail
from django.conf import settings

def Register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('password2')


        if not (len(password) >= 8 and any(char.isupper() for char in password) and any(char in '!@#$%^&*()-_=+' for char in password)):
            messages.error(request, 'Password must be at least 8 characters with 1 uppercase letter and 1 special character.')
            return render(request, 'register.html', {'username': username, 'email': email})

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html', {'username': username, 'email': email})



        if RegisterDB.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please use a different email.')
            return render(request, 'register.html', {'username': username, 'email': email})

        if RegisterDB.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return render(request, 'register.html', {'username': username, 'email': email})


        obj = RegisterDB(username=username, email=email, password=password,confirm_password=confirm_password)
        obj.save()

        subject = 'Account Activation'
        message = f'Thank you for registering with us, {username}! Your account has been successfully created.'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [email]
        send_mail(subject, message, from_email, to_email, fail_silently=False)

        messages.success(request, 'User registered successfully! Confirmation email sent.')
        return redirect(loginpage)

    return render(request, 'register.html')


def loginpage(request):
    return render(request,"loginpage.html")

def user(request):
    if request.session.get('email'):
        username = request.session['email']
        datas = RegisterDB.objects.get(email=username)
    return render(request,"user.html",{"datas":datas})

def userpage(request):
    if request.method == 'POST':
        email_r = request.POST.get('email')
        password = request.POST.get('password')

        if RegisterDB.objects.filter(email=email_r, password=password).exists():
            data = RegisterDB.objects.get(email=email_r)
            request.session['email'] = email_r
            request.session['password'] = password
            request.session['is_admin'] = False
            return redirect(user)

        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'loginpage.html')

def logout(request):
    if 'password' in request.session:
        del request.session['password']
    if 'email' in request.session:
        del request.session['email']
    return redirect(loginpage)

def edit(request):
    datas = None
    if request.session.get('email'):
        username = request.session['email']
        datas = RegisterDB.objects.get(email=username)
    return render(request,"changepassword.html",{'datas': datas})


def updatepassword(request):
    datas = None

    if request.session.get('email'):
        username = request.session['email']

        if request.method == "POST":
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")


            if password == confirm_password and len(password) >= 8 and any(char.isupper() for char in password) and any(char in '!@#$%^&*()-_=+' for char in password):
                RegisterDB.objects.filter(email=username).update(password=password, confirm_password=confirm_password)

                subject = 'Password Update'
                message = f' {username}! Your account Password Changed.'
                from_email = settings.DEFAULT_FROM_EMAIL
                to_email = [username]
                send_mail(subject, message, from_email, to_email, fail_silently=False)

                messages.success(request, 'Password updated successfully!')
                return redirect('user')
            else:
                messages.error(request, 'Invalid password. Please ensure it meets the criteria: at least 8 characters, 1 uppercase letter, and 1 special character.')

    return redirect('edit')

