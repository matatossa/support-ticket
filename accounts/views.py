import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
import uuid

from .forms import RegisterationFrom, UserForm, UserProfileForm
from .models import Account, UserProfile
from .token import account_activation_token
def home(request):
    render(request,'home.html')
def register(request):
    if request.method == "POST":
        form = RegisterationFrom(request.POST)
        if form.is_valid():
            
            phone_number = form.cleaned_data['Phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            role=form.cleaned_data['role']
            user = Account.objects.create_user( email=email,  password=password,role=role)
            user.Phone_number = phone_number
            user.save()
            
            
            profile = UserProfile()
            profile.user_id = user.id
            profile.save()

           
            current_site = get_current_site(request)
            subject = 'Please activate your account'
            message = render_to_string('accounts/email_activate/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(subject, message, to=[to_email])
            send_email.send()
    
            return redirect('/accounts/register/?command=verification&email='+email)
    else:
        form = RegisterationFrom()

    context = {
        'forms': form,
    }

    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == "POST":
        print("POST request received")  

        email = request.POST.get('email')
        password = request.POST.get('password')
        
        print(f"Email: {email}, Password: {password}")  

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            print(f"Authenticated user: {user.email}, Role: {user.role}")  

            auth.login(request, user)
            if user.role == 'admin':
                print("Redirecting to admin side...")  
                return redirect('support:adminside')
            elif user.role == 'client':
                print("Redirecting to client side...") 
                return redirect('support:clientside')
        else:
            print("Authentication failed") 
            messages.error(request, 'Your email or password is incorrect!')
            return redirect('accounts:login')

    print("Rendering login page") 
    return render(request, 'accounts/login.html')


@login_required(login_url='accounts:login')
def logout(request):
    auth.logout(request)
    messages.success(request, "You've successfully logged out. Come back soon!")
    return redirect('accounts:login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account is activated, log in and let's go.")
        return redirect('accounts:login')
    else:
        messages.error(request, "Invalid activation link, Try again!")
        return redirect('accounts:register')

@login_required(login_url='accounts:login')
def dashboard(request):
    profile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'profile': profile,
    }
    return render(request, 'accounts/dashboard/dashboard.html', context)

@login_required(login_url='accounts:login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('accounts:edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/dashboard/edit_profile.html', context)

@login_required(login_url='accounts:login')
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        repeat_new_password = request.POST['repeat_new_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == repeat_new_password:
            success = user.check_password(old_password)
            if success:
                user.set_password(new_password)
                user.save()
                auth.login(request, user)
                messages.success(request, 'Password Updated successfully.')
                return redirect('accounts:change_password')
            else:
                messages.error(request, 'Old password is wrong')
                return redirect('accounts:change_password')
        else:
            messages.error(request, 'Password does not match')
            return redirect('accounts:change_password')
    return render(request, 'accounts/dashboard/change_password.html')

def forget_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            
          
            current_site = get_current_site(request)
            subject = 'Reset Your Password'
            message = render_to_string('accounts/forget_password/send_resetpassword_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(subject, message, to=[to_email])
            send_email.send()

            return redirect('/accounts/forget_password/?command=resetpassword&email='+email)
        else:
            messages.error(request, 'This email does not exist!')
            return redirect('accounts:forget_password')

    return render(request, 'accounts/forget_password/forget_password.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        request.session['uid'] = uid
        return redirect('accounts:reset_password')
    else:
        messages.error(request, 'This link has expired!')
        return redirect('accounts:forget_password')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        repeat_password = request.POST['confirm_password']

        try:
            if password == repeat_password:
                uid = request.session.get('uid')
                user = Account.objects.get(pk=uid)
                user.set_password(password)
                user.save()
                messages.success(request, 'Password Reset Successful')
                return redirect('accounts:login')
            else:
                messages.error(request, "Password does not match!")
                return redirect('accounts:reset_password')
        except Account.DoesNotExist:
            messages.error(request, "Please enter your email address here first!")
            return redirect('accounts:forget_password')
    else:
        return render(request, 'accounts/forget_password/reset_password.html')
    
    
