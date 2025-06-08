from django.shortcuts import render
from authentication.decorators import login_required_custom

@login_required_custom
def index(request):
    return render(request, 'homepage/index.html')