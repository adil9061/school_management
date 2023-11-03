from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse

def admin_required(view_func):
    @wraps(view_func)
    def check_admin(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_principle:
            return view_func(request, *args, **kwargs)
        elif not request.user.is_authenticated:
            return redirect(reverse('custom_login'))
        else:
            return redirect('no_permission')
    return check_admin

class AdminRequiredMixin:
    @classmethod
    def as_view(cls, *init_args, **init_kwargs):
        view = super().as_view(*init_args, **init_kwargs)
        return admin_required(view)

