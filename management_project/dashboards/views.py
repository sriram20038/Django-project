from django.shortcuts import render, redirect, get_object_or_404
from .models import TrainingRequest,Course,Module
from authentication.models import User,Role
from .forms import TrainingRequestForm,CourseForm
from django.contrib import messages
from django.core.paginator import Paginator


# Create your views here.
def Admin_view(request, user_id):
    admin = get_object_or_404(User, id=user_id)

    if request.method == 'POST' and 'delete_course' in request.POST:
        course_id = request.POST.get('course_id')
        course = get_object_or_404(Course, course_id=course_id)
        course.delete()
        return redirect('Admin', user_id=user_id)  # Redirect to the admin page after deletion

    context = {
        'name': admin.name,
        'user_id': user_id,
        'courses_count': Course.objects.all().count(),
        'pending_count': TrainingRequest.objects.filter(status='Pending').count(),
        'employees_count': User.objects.filter(role=Role.objects.get(role_name='Employee').id).count(),
        'pending_requests': TrainingRequest.objects.filter(status='Pending'),
        'courses': Course.objects.all(),
    }
    return render(request, 'dashboards/Admin.html', context)


def admin_action(request, user_id, request_id):
    task = get_object_or_404(TrainingRequest, request_id=request_id)
    context = {
        'title': task.title,
        'description': task.description,
        'account_manager': task.account_manager
    }

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            task.status = 'Approved'
            task.save()
            return redirect('create_course', user_id=user_id)  # Correct the redirect to pass user_id properly

        elif action == 'reject':
            task.status = 'Rejected'
            task.save()
            return redirect('Admin', user_id=user_id)  # Correct the redirect to pass user_id properly

    return render(request, 'dashboards/admin_action.html', context)


def create_course(request, user_id):
    create=User.objects.get(id=user_id)
    if request.method == 'POST':
        form = CourseForm(request.POST)
        
        if form.is_valid():
            course = form.save(commit=False)  # Don't save to the database yet
            course.created_by = create  # Assign the logged-in user
            course.save()  # Save to the database
            messages.success(request, 'Course created successfully!')
            return redirect('view_course', course_id=course.course_id)

    else:
        form = CourseForm()

    return render(request, 'dashboards/create_course.html', {'form': form})


def view_course(request,course_id):
    course = get_object_or_404(Course, course_id=course_id)
    import re

    def extract_video_id(url):
        # Regular expression to match YouTube URL formats
        patterns = [
            r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',  # For standard YouTube URLs
            r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]{11})'  # For shortened URLs
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)  # Return the video ID

        return None  # Return None if no ID is found

    # Example Usage
    url = course.resource_link
    video_id = extract_video_id(url)


    context={
        'course':course,
        'video_id':video_id

    }
    return render(request, 'dashboards/view_course.html', context)




def Employee_view(request,user_id):
    employee = get_object_or_404(User, id=user_id)
    context={
        'employee':employee,
        'courses':Course.objects.all()
    }
    return render(request, 'dashboards/Employee.html',context)
def Manager_view(request, user_id):
    manager = get_object_or_404(User, id=user_id)
    training_requests = TrainingRequest.objects.filter(account_manager=manager).order_by('-created_at')
    limit = int(request.GET.get('limit', 5))
    offset = int(request.GET.get('offset', 0))


    # Use Paginator to manage data
    paginator = Paginator(training_requests, limit)
    page_number = offset // limit + 1
    page = paginator.get_page(page_number)
    
    context = {
        'name': manager.name,
        'total': training_requests.count(),
        'completed': training_requests.filter(status='Approved').count(),
        'pending': training_requests.filter(status='Pending').count(),
        'data': page,
    }

    if request.method == 'POST':
        form = TrainingRequestForm(request.POST)
        if form.is_valid():
            # Create a TrainingRequest instance but don't save it yet
            instance = form.save(commit=False)
            instance.account_manager = manager  # Set the account manager
            instance.save()  # Save the instance to the database
            return redirect("Manager", user_id=user_id)
        else:
            print(form.errors)  # Print errors for debugging
    else:
        form = TrainingRequestForm()

    context['form'] = form
    return render(request, 'dashboards/Manager.html', context)