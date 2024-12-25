from django import forms
from .models import TrainingRequest, Course, Feedback,GeneralFeedback

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
        fields = ['title', 'description','resource_link']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comments']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'comments': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your comments here...', 
                'rows': 4
            }),
        }
        labels = {
            'course': 'Course',
            'rating': 'Rate the course (1 to 5)',
            'comments': 'Additional Comments',
        }



class GeneralFeedbackForm(forms.ModelForm):
    class Meta:
        model = GeneralFeedback
        fields = ['comments']
        widgets = {
            'comments': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Enter your feedback here...',
                'class': 'form-control',
            }),
        }
