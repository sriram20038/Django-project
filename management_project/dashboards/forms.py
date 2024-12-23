from django import forms
from authentication.models import User
from django.forms import inlineformset_factory
from .models import TrainingRequest, Course, Module

class TrainingRequestForm(forms.ModelForm):
    class Meta:
        model = TrainingRequest
        fields = ['title', 'description', 'course_duration', 'employee_count']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'status': forms.Select(),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'resources']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }
