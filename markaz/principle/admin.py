from django.contrib import admin
from principle.models import *
# Register your models here.
# class CustomUserAdmin(admin.ModelAdmin):
#     exclude = ('first_name', 'last_name', 'groups')

# admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Teacher)

admin.site.register(Student)

admin.site.register(Courses)

admin.site.register(Exam)

admin.site.register(Subject)

admin.site.register(AcademicDetail)

admin.site.register(Certificate)

admin.site.register(Announcement)

admin.site.register(Country)

admin.site.register(State)

admin.site.register(City)

admin.site.register(Room)

admin.site.register(Message)

