from django import forms
from Study_Resources.models import Resource

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'url', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }
