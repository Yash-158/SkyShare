# accounts/views.py
import uuid
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse

from .forms import (
    CustomUserCreationForm, 
    CustomLoginForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm
)

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.email_verified = False
            
            # Generate verification token
            token = str(uuid.uuid4())
            user.verification_token = token
            user.save()
            
            # Send verification email
            mail_subject = 'Activate your account'
            message = render_to_string('accounts/email/account_activation_email.html', {
                'user': user,
                'domain': request.get_host(),
                'token': token,
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.content_subtype = 'html'
            email.send()
            
            messages.success(request, 'Please confirm your email address to complete the registration.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def verify_email(request, token):
    try:
        user = User.objects.get(verification_token=token)
        user.email_verified = True
        user.verification_token = None
        user.save()
        messages.success(request, 'Your email has been verified. You can now login.')
    except User.DoesNotExist:
        messages.error(request, 'Invalid verification link.')
    
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            
            try:
                user = User.objects.get(email=email)
                if not user.email_verified:
                    messages.error(request, 'Please verify your email before logging in.')
                    return render(request, 'accounts/login.html', {'form': form})
            except User.DoesNotExist:
                pass
                
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = CustomLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

def password_reset_request(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    token = default_token_generator.make_token(user)
                    reset_url = request.build_absolute_uri(
                        reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                    )
                    
                    message = render_to_string("accounts/email/password_reset_email.html", {
                        'user': user,
                        'reset_url': reset_url  # Use the pre-built URL instead of constructing in template
                    })
                    email = EmailMessage(subject, message, to=[user.email])
                    email.content_subtype = 'html'
                    email.send()
                    
                messages.success(request, 'We\'ve emailed you instructions for setting your password.')
                return redirect('login')
            else:
                messages.error(request, 'No user with that email address found.')
    else:
        form = CustomPasswordResetForm()
    
    return render(request, 'accounts/password_reset.html', {'form': form})

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = CustomSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been set. You may log in now.')
                return redirect('login')
        else:
            form = CustomSetPasswordForm(user)
        return render(request, 'accounts/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, 'The reset link is invalid or has expired.')
        return redirect('login')

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')