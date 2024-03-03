from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .models import Profile
import random

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user.is_active and user.is_staff and user.is_superuser:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect(reverse('admin:index'))
        elif user.is_active:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('home')
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    return redirect("login")

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match.')
        else:
            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password1)
            
            # Generate OTP
            otp = random.randint(100000, 999999)
            print('hello', otp)
            
            # Save OTP to user's profile
            profile = Profile(user=user, token=otp)
            profile.save()
            
            # Send verification email
            subject = 'Your Account Verification OTP'
            message = f'Hi, here is your account verification OTP: {otp}'
            email_from = settings.EMAIL_HOST_USER
            recipient = [email]
            
            try:
                send_mail(subject, message, email_from, recipient)
                messages.success(request, 'Account created successfully. Please verify your email.')
                return redirect('otp_verify')  # Redirect to the login page after successful registration
            except Exception as e: # Rollback user creation if email sending fails
                profile.delete()
                user.delete()
                messages.error(request, f'Failed to send OTP: {str(e)}')

    return render(request, 'accounts/register.html')

def otp_verify(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        try:
            profile = Profile.objects.get(token=otp)
            profile.is_verified = True
            profile.save()
            messages.success(request, 'Email verified successfully.')
            return redirect('login')  # Redirect to login page after successful verification
        except Profile.DoesNotExist:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('register')  # Redirect to register page for invalid OTP
    return render(request, 'accounts/OTP.html')

def change_pass(request):
    if request.method == 'POST':
        old_pass = request.POST.get('old_password')
        new_pass = request.POST.get('new_password1')
        new_pass2 = request.POST.get('new_password2')
        user = request.user

        if not user.check_password(old_pass):
            messages.error(request, 'Old password is incorrect.')
        elif new_pass != new_pass2:
            messages.error(request, 'New passwords do not match.')
        else:
            user.set_password(new_pass)
            user.save()
            messages.success(request, 'Password updated successfully.')
            return redirect('login')

    return render(request, 'accounts/changePass.html')

'''
def reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')

        try:
            user = User.objects.get(email=email, username=username)
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or username.')
            return render(request, 'accounts/reset.html')

        otp = random.randint(100000, 999999)

        try:
            profile = Profile.objects.get(user=user)
            profile.token = otp
            profile.save()
        except Profile.DoesNotExist:
            profile = Profile(user=user, token=otp)
            profile.save()

        subject = 'Your Password Reset OTP'
        message = f'Hi, here is your password reset OTP: {otp}'
        email_from = settings.EMAIL_HOST_USER
        recipient = [email]

        try:
            send_mail(subject, message, email_from, recipient)
            messages.success(request, 'An OTP has been sent to your email. Please check and verify.')
            return redirect('otp_verify_reset')
        except Exception as e:
            if not profile.pk:
                profile.delete()
            messages.error(request, f'Failed to send OTP: {str(e)}')

    return render(request, 'accounts/reset.html')

def otp_verify_reset(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        try:
            profile = Profile.objects.get(token=otp)
            if not profile.is_verified:
                messages.error(request, 'Email not verified. Please verify your email first.')
                return redirect('reset')
            profile.is_reset = True
            profile.save()
            # Redirect to password update page with OTP included
            return redirect(reverse('update_pass') + '?otp=' + otp)
        except Profile.DoesNotExist:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('reset')
    return render(request, 'accounts/resetOTP.html')

def update_pass(request):
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        otp = request.GET.get('otp')  # Retrieve OTP from GET parameters

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/newPass.html')

        try:
            profile = Profile.objects.get(token=otp)
            user = profile.user
            user.set_password(password1)
            user.save()
            messages.success(request, 'Password updated successfully.')
            return redirect('login')
        except Profile.DoesNotExist:
            messages.error(request, 'Invalid OTP. Please try again.')
            return render(request, 'accounts/newPass.html')

    return render(request, 'accounts/newPass.html')
'''
