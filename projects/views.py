from django.shortcuts import render, redirect
from .models import Project
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required


def projects(request):
    projs = Project.objects.all()
    return render(request, 'projects/projects.html', {'projects': projs})


def project(request, pk):
    proj = Project.objects.get(pk=pk)
    return render(request, 'projects/single-project.html', {'project': proj})


@login_required(login_url='login')
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            proj = form.save(commit=False)
            form.owner = profile
            proj.save()
            return redirect('projects')
    return render(request, 'projects/create-project.html', {'form': form})


def update_project(request):
    return None