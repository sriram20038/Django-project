from django.db import models

class TrainingRequest(models.Model):
    request_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=[('Pending', 'Pending'),
                 ('Approved', 'Approved'),
                 ('Rejected', 'Rejected')],  # Only 'Pending' by default
        default='Pending'
    )
    account_manager = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        limit_choices_to={'role__role_name': 'Manager'}
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class course(models.Model):
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
    resources = models.URLField(max_length=1024, null=True, blank=True)  # New field for resources

    def __str__(self):
        return self.title