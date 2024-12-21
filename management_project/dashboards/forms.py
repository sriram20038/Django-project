from django import forms
from authentication.models import User
from .models import TrainingRequest,course

class RequestForm(forms.ModelForm):
    class Meta:
        model = TrainingRequest
        fields = ['title', 'description']  # Exclude 'account_manager' since it will be handled in the view


class CourseForm(forms.ModelForm):
    # Adding a custom field for selecting employees
    employees = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role__role_name='Employee'), 
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    
    class Meta:
        model = course
        fields = ['title', 'description', 'resources', 'employees']  # Include fields you want in the form
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }