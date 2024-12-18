from django import forms
from .models import TrainingRequest

class RequestForm(forms.ModelForm):
    class Meta:
        model = TrainingRequest
        fields = ['title', 'description']  # Exclude 'account_manager' since it will be handled in the view
