from django.db import models
from django.contrib.auth.models import AbstractUser
from principle.models import *
from django.utils import timezone
# Create your models here.

class CustomUser(AbstractUser):

    is_principle = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_active =models.BooleanField(default=True)
    
    email = models.EmailField(unique=True)

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
    