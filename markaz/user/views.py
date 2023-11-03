from django.shortcuts import render, redirect
from principle.views import *
from django.contrib import messages
import random
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.http import HttpResponse
from student.urls import *
from teacher.urls import *
from django.utils import timezone

# Create your views here.

def checkpath(request):
    if request.user.is_authenticated:
        if request.user.is_principle:
            return redirect('admin-home')
        elif request.user.is_student:
            return redirect('student_home')
        elif request.user.is_teacher:
            return redirect('teacher_home')
        else:
            pass
    else:
        return redirect('custom_login')


# Login With OTP


def send_otp_email(email, otp):
    subject = 'Your otp for login'
    message = f'Your otp for login is {otp}'
    from_email = 'dhilu6927@gmail.com'
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)

def generate_otp():
    return str(random.randint(100000, 999999))

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        user = authenticate(request, username=username, password=password)
        
        if CustomUser.objects.filter(username=username, email=email, password=password).exists():
            user = CustomUser.objects.get(username=username, email=email)
            if not user.is_active:
                error_message = "Your account is not active. Please contact the administrator."
                return render(request, 'user/login.html', {'error_message': error_message})

            if not (user.is_principle or user.is_teacher or user.is_student):
                error_message = "You do not have the necessary roles to access this system."
                return render(request, 'user/login.html', {'error_message': error_message})

            # Generate the OTP
            otp = generate_otp()
            send_otp_email(email, otp)
            request.session['otp'] = otp

            user.update_at = timezone.now()
            user.save()

            return render(request, 'user/otp_verification.html', {'username': username, 'email': email})
        else:
            error_message = "Incorrect username, password or email. Please try again."
            return render(request, 'user/login.html', {'error_message': error_message})

    return render(request, 'user/login.html')


def otp_verification_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        entered_otp = request.POST.get('otp')

        saved_otp = request.session.get('otp')

        if saved_otp == entered_otp:
            user = CustomUser.objects.get(username=username, email=email)
            login(request, user)
            if user.is_principle:
                return redirect('admin-home')
            elif user.is_teacher:
                return redirect('teacher_home')
            elif user.is_student:
                return redirect('student_home')
        else:
            error_message = "Invalid OTP. Please try again..!!"
            return render(request, 'user/login.html', {'error_message': error_message})

    
    return HttpResponse('Invalid request', status=400)