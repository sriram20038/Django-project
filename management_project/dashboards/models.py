from django.db import models
from django.db.models import Count

class TrainingRequest(models.Model):
    request_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=[('Pending', 'Pending'),
                 ('Approved', 'Approved'),
                 ('Rejected', 'Rejected')],
        default='Pending'
    )
    account_manager = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        limit_choices_to={'role__role_name': 'Manager'}
    )
    course_duration = models.PositiveIntegerField(help_text="Duration in days")  # New field
    employee_count = models.PositiveIntegerField(help_text="Number of employees involved")  # New field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        limit_choices_to={'role__role_name': 'Admin'}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    employees = models.ManyToManyField(
        'authentication.User',
        related_name='enrolled_courses',
        limit_choices_to={'role__role_name': 'Employee'},
        blank=True  # Optional field
    )
    resources = models.URLField(max_length=1024, null=True, blank=True)  # General course resources

    def number_of_modules(self):
        # Count the number of related modules
        return self.modules.count()

    def __str__(self):
        return self.title

class Module(models.Model):
    module_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(
        Course,
        related_name='modules',  # Links modules to a course
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    resources = models.URLField(max_length=1024, null=True, blank=True)  # Resources specific to this module
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"
