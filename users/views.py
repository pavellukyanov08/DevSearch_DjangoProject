from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth import logout


def login_user(request):
    return render(request, 'users/login.html')


def logout_user(request):
    logout(request)
    return redirect('login')


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

