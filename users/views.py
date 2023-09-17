from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Profile, User
from django.contrib.auth import logout, login, authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .forms import ProfileForm, CustomUserCreationForm


def login_user(request):
    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            messages.error(request, 'Такого пользователя не существует')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')

    return render(request, 'users/login_register.html')


def logout_user(request):
    logout(request)
    return redirect('login')


def register_user(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower().strip()
            user.save()
            messages.success(request, 'Аккаунт был создан')
            login(request, user)
            return redirect('profiles')

    return render(request, 'users/login_register.html', {'page': page, 'form': form})


def profiles(request):
    profs = Profile.objects.all()
    context = {'profiles': profs}
    return render(request, 'users/index.html', context)


def user_profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    top_skills = profile.skill_set.exclude(description__exact='')
    other_skills = profile.skill_set.filter(description__exact='')
    context = {
        'top_skills': top_skills,
        'other_skills': other_skills,
    }
    return render(request, 'users/profile.html', {'profile': profile})


@login_required
def user_account(request):
    prof = request.user.profile
    skills = prof.skill_set.all()
    projects = prof.project_set.all()
    context = {
        'profile': prof,
        'skills': skills,
        'projects': projects,
    }

    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            messages.success(request, 'Account edited successfully!')
            return redirect('account')
    return render(request, 'users/profile_form.html', {'form': form})
