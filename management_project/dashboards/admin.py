from django.contrib import admin
from .models import TrainingRequest, Course, Module,Progress,Feedback,GeneralFeedback

@admin.register(TrainingRequest)
class TrainingRequestAdmin(admin.ModelAdmin):
    list_display = ('request_id', 'title', 'status', 'account_manager', 'course_duration', 'employee_count', 'created_at')
    list_filter = ('status', 'account_manager', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'title', 'created_by', 'created_at')
    list_filter = ('created_by', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    filter_horizontal = ('employees',)  # For easier management of ManyToManyField


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('module_id', 'course', 'title', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('progress_id', 'course', 'employee', 'progress_percent')
    search_fields = ('course__name', 'employee__username')  # Adjust based on actual fields in Course and User models
    list_filter = ('progress_percent',)  # Filter by progress percentage

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('feedback_id', 'course', 'employee', 'rating', 'comments')
    search_fields = ('course__name', 'employee__username')  # Adjust based on actual fields in Course and User models
    list_filter = ('rating',)  # Filter by rating


@admin.register(GeneralFeedback)
class GeneralFeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'comments', 'submitted_at')  # Columns displayed in the admin list view
    list_filter = ('submitted_at',)  # Filters for the admin interface
    search_fields = ('user__username', 'comments')  # Fields for the search bar
    ordering = ('-submitted_at',)  # Default ordering by submission date (newest first)

    def get_queryset(self, request):
        # Customize the queryset if needed (e.g., for filtering by user permissions)
        return super().get_queryset(request).select_related('user')