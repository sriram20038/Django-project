from django.contrib import admin
from .models import TrainingRequest,course

@admin.register(TrainingRequest)
class TrainingRequestAdmin(admin.ModelAdmin):
    list_display = ('request_id', 'title', 'status', 'account_manager')
    list_filter = ('status',)
    search_fields = ('title', 'description')
    actions = ['approve_requests', 'reject_requests']

    @admin.action(description='Approve selected training requests')
    def approve_requests(self, request, queryset):
        queryset.update(status='Approved')

    @admin.action(description='Reject selected training requests')
    def reject_requests(self, request, queryset):
        queryset.update(status='Rejected')

# Customize the display of the courses model in the admin panel
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'title', 'created_by', 'created_at', 'get_employees', 'resources')
    search_fields = ('title', 'description', 'created_by__username')
    list_filter = ('created_at', 'created_by')
    
    # Custom method to display the enrolled employees as a comma-separated list
    def get_employees(self, obj):
        return ", ".join([employee.username for employee in obj.employees.all()])
    get_employees.short_description = 'Enrolled Employees'  # This is the column header name

# Register the model with the custom admin configuration
admin.site.register(course, CourseAdmin)