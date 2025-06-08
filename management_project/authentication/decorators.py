from functools import wraps
from django.shortcuts import redirect
from .models import User # Assuming User model is in the same app (authentication)

def login_required_custom(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('login')  # Name of your login URL pattern
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user_id = request.session.get('user_id')
            if not user_id:
                return redirect('login')
            
            try:
                user = User.objects.get(id=user_id)
                if user.role.role_name not in allowed_roles:
                    # For simplicity, redirecting to login.
                    # A 'permission_denied' page would be more user-friendly.
                    return redirect('login') 
            except User.DoesNotExist:
                return redirect('login') # Should not happen if session is valid
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
