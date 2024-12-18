from django.urls import path
from . import views

urlpatterns = [
    
    path('Admin/<int:user_id>/', views.Admin_view, name='Admin'),
    path('Employee/<int:user_id>', views.Employee_view, name='Employee'),
    path('Manager/<int:user_id>', views.Manager_view, name='Manager'),
]