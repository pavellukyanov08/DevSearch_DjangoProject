from django.shortcuts import render, redirect
from .models import Project
from .forms import ProjectForm


def projects(request):
    projs = Project.objects.all()
    return render(request, 'projects/projects.html', {'projects': projs})


def project(request, pk):
    proj = Project.objects.get(pk=pk)
    return render(request, 'projects/single-project.html', {'project': proj})


def create_project(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projects')
    return render(request, 'projects/create-project.html', {'form': form})
