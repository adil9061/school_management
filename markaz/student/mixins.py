from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse



def student_required(view_func):
    @wraps(view_func)
    def check_student(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_student:
            return view_func(request, *args, **kwargs)
        elif not request.user.is_authenticated:
            return redirect(reverse('custom_login'))
        else:
            return redirect('no_permission')
    return check_student

class StudentRequiredMixin:
    @classmethod
    def as_view(cls, *init_args, **init_kwargs):
        view = super().as_view(*init_args, **init_kwargs)
        return student_required(view)