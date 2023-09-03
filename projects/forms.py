from django.forms import ModelForm
from .models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['vote_ratio', 'vote_total', 'created']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)