from django.contrib import admin
from user.models import *
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    exclude = ('first_name', 'last_name', 'groups')

admin.site.register(CustomUser, CustomUserAdmin)
