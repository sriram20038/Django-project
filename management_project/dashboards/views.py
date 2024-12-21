from django.shortcuts import render, redirect, get_object_or_404
from .models import TrainingRequest,course
from authentication.models import User,Role
from .forms import RequestForm,CourseForm
from django.contrib import messages

# Create your views here.
def Admin_view(request,user_id):
    admin = get_object_or_404(User, id=user_id)
    context={
        'name':admin.name,
        'user_id':user_id,
        'courses_count':course.objects.all().count(),
        'pending_count':TrainingRequest.objects.filter(status='Pending').count(),
        'employees_count':User.objects.filter(role=Role.objects.get(role_name='Employee').id).count(),
        'pending_requests':TrainingRequest.objects.filter(status='Pending'),
        'approved_requests':TrainingRequest.objects.filter(status='Approved'),

    }
    return render(request, 'dashboards/Admin.html',context)

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
            return redirect('Admin', user_id=user_id)

    else:
        form = CourseForm()

    return render(request, 'dashboards/create_course.html', {'form': form})


def Employee_view(request):
    return render(request, 'dashboards/Employee.html')
def Manager_view(request, user_id):
    manager = get_object_or_404(User, id=user_id)
    training_requests = TrainingRequest.objects.filter(account_manager=manager)
    
    context = {
        'name': manager.name,
        'total': training_requests.count(),
        'completed': training_requests.filter(status='Approved').count(),
        'pending': training_requests.filter(status='Pending').count(),
        'data': training_requests,
    }

    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            # Create a TrainingRequest instance but don't save it yet
            instance = form.save(commit=False)
            instance.account_manager = manager  # Set the account manager
            instance.save()  # Save the instance to the database
            return redirect("Manager", user_id=user_id)
        else:
            print(form.errors)  # Print errors for debugging
    else:
        form = RequestForm()

    context['form'] = form
    return render(request, 'dashboards/Manager.html', context)