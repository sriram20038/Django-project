from django.urls import path
from . import views

urlpatterns = [
    
    path('Admin/<int:user_id>/', views.Admin_view, name='Admin'),
    path('Employee/<int:user_id>', views.Employee_view, name='Employee'),
    path('Manager/<int:user_id>', views.Manager_view, name='Manager'),
    path('admin_action/<int:user_id>/<int:request_id>/', views.admin_action, name='admin_action'),
    path('create_course/<int:user_id>/', views.create_course, name='create_course'),
]