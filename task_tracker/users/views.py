from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .forms import SignUpForm, UserPasswordChangeForm ,UserProfileForm ,CustomUserChangeForm
from .models import UserProfile
from django.contrib.auth.forms import UserChangeForm

def home(request):
    # Anasayfa görüntüleme
    return render(request,'home.html')

@login_required
def view_profile(request):
    # Kullanıcının profilini görüntüleme ve güncelleme
    user = request.user
    user_profile = user.userprofile
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profiliniz başarıyla güncellendi.')
            return redirect('users:view_profile')
        else:
            messages.error(request, 'Formda hata oluştu. Lütfen tekrar deneyin.')
    else:
        user_form = CustomUserChangeForm(instance=user)
        profile_form = UserProfileForm(instance=user_profile)
    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def edit_profile(request):
    # Profil düzenleme
    user = request.user
    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Profiliniz başarıyla güncellendi.')
            return redirect('users:view_profile')
        else:
            messages.error(request, 'Formda hata oluştu. Lütfen tekrar deneyin.')
    else:
        user_form = UserChangeForm(instance=user)
    return render(request, 'users/profile.html', {'user_form': user_form})

@login_required
def change_password(request):
    # Şifre değiştirme
    if request.method == 'POST':
        form = UserPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Şifreniz başarıyla değiştirildi. Yeniden giriş yapmayı unutmayın.')
            logout(request)
            return redirect('login')
        else:
            messages.error(request, 'Formda hata oluştu. Lütfen tekrar deneyin.')
    else:
        form = UserPasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Başarıyla kayıt oldunuz. Hoş geldiniz!')
                return redirect('users:login')
        else:
            messages.error(request, 'Formda hata oluştu. Lütfen tekrar deneyin.', extra_tags='danger')
    else:
        form = SignUpForm()
    return render(request, 'users/register.html', {'form': form})

