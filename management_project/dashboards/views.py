from django.shortcuts import render, redirect, get_object_or_404
from .models import TrainingRequest
from authentication.models import User
from .forms import RequestForm

# Create your views here.
def Admin_view(request):
    return render(request, 'dashboards/Admin.html')

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