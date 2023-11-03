from django.shortcuts import render, redirect
from principle.views import *
from django.contrib.auth.decorators import login_required
from teacher.models import *
from teacher.forms import *
from django.db.models import Sum
from django.contrib.auth import authenticate, login, logout
from django.utils.timezone import now
from django.views import View
from datetime import datetime, time
import pytz
from datetime import timedelta
from django.utils import timezone
from django.http import JsonResponse, HttpResponseForbidden, FileResponse
from django.views.generic import FormView, ListView
from django.views import View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from teacher.mixins import teacher_required, TeacherRequiredMixin

# Create your views here.

def no_permission(request):
    return render(request, 'teacher/no_permission.html')

# Teacher Home

class TeacherHomeView(TeacherRequiredMixin,View):
    def get(self, request):
        return render(request, 'teacher/teacherhome.html')
# Add Study Materials

class AddStudyMaterialView(TeacherRequiredMixin,FormView):
    template_name = 'teacher/add_study_material.html'

    def get(self, request):
        form = StudyMaterialForm()
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = StudyMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            study_material = form.save(commit=False)
            study_material.teacher = request.user.teacher
            study_material.save()
            return redirect('teacher_home')

        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

# Study Material List, Update, Delete


class UploadedStudyMaterialList(View):
    def get(self, request):
        study_materials = StudyMaterial.objects.filter(teacher=request.user.teacher)
    
        context = {
            'study_materials': study_materials,
        }
    
        return render(request, 'teacher/uploded_materials.html', context)

class ViewMaterials(TeacherRequiredMixin,View):

    def get(self, request, material_id):
        material = get_object_or_404(StudyMaterial, pk=material_id)
        response = FileResponse(material.file)
        return response

class UpdateStudyMaterial(TeacherRequiredMixin, View):
    template_name = 'teacher/update_study_material.html'


    def get(self, request, material_id):
        material = StudyMaterial.objects.get(pk=material_id)
        form = StudyMaterialForm(instance=material)
        context = {
            'form': form,
            'material': material,
        }
        return render(request, self.template_name, context)

    def post(self, request, material_id):
        material = StudyMaterial.objects.get(pk=material_id)
        form = StudyMaterialForm(request.POST, request.FILES, instance=material)

        if form.is_valid():
            form.instance.teacher = request.user.teacher
            form.save()
            return redirect('uploded_materials')
        else:
            context = {
                'form': form,
                'material': material,
            }
            return render(request, self.template_name, context)

class DeleteStudyMaterial(TeacherRequiredMixin,View):
    template_name = 'teacher/delete_study_material.html'

    def get(self, request, material_id):
        material = get_object_or_404(StudyMaterial, pk=material_id)
        context = {'material': material}
        return render(request, self.template_name, context)

    def post(self, request, material_id):
        material = get_object_or_404(StudyMaterial, pk=material_id)
        material.delete()
        return redirect('teacher_home')

# Submit Attendance

class MarkAttendance(TeacherRequiredMixin,View):

    def get(self, request):

        teacher = request.user.teacher
        today = datetime.now().date()
        morning_start_time = time(7, 0) 
        afternoon_start_time = time(12, 0) 

        current_time = datetime.now().time()

        time_allowed_for_morning = current_time >= morning_start_time and current_time < afternoon_start_time

        time_allowed_for_afternoon = current_time >= afternoon_start_time

        try:
            attendance = TeacherAttendance.objects.get(teacher=teacher, date=today)

        except TeacherAttendance.DoesNotExist:

            attendance = TeacherAttendance(teacher=teacher, date=today)
            attendance.save()

        return render(request, 'teacher/mark_attendance.html', {
            'attendance': attendance,
            'time_allowed_for_morning': time_allowed_for_morning,
            'time_allowed_for_afternoon': time_allowed_for_afternoon,
        })


    def post(self, request):

        current_time = datetime.now().time()
        morning_start_time = time(7, 0)

        afternoon_start_time = time(12, 0)

        teacher = request.user.teacher
        today = datetime.now().date()

        if current_time > morning_start_time and current_time < afternoon_start_time:
            attendance_type = 'morning_attendance'

        elif current_time >= afternoon_start_time:
            attendance_type = 'afternoon_attendance'
        else:
            return render(request, 'teacher/error.html', {'message' : 'Attendance submission not allowed at this time'})


        try:
            attendance = TeacherAttendance.objects.get(teacher=teacher, date=today)
            setattr(attendance, attendance_type, request.POST.get(attendance_type) == 'on')
            attendance.save()
        except TeacherAttendance.DoesNotExist:

            attendance_data = {
                'teacher' : teacher,
                'date' : today,
                attendance_type : request.POST.get(attendance_type) == 'on'

            }
            attendance = TeacherAttendance(**attendance_data)
            attendance.save()

        return redirect('teacher_home')

# View Announcements

class TeacherAnnouncements(TeacherRequiredMixin,ListView):
    model = Announcement
    template_name = 'teacher/teacher_announcements.html'
    context_object_name = 'announcements'

    def get_queryset(self):
        one_day = timezone.now() - timedelta(days=1)
        return Announcement.objects.filter(created_at__gte=one_day, show_to_teachers=True)

# Send Notification

class SendNotification(TeacherRequiredMixin,View):
    template_name = 'teacher/send_notification.html'

    def get(self, request):
        form = NotificationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.instance.sender = request.user.teacher
            form.save()
            return redirect('teacher_home')
        return render(request, self.template_name, {'form': form})

# List, Update, Delete Notification

class ListNotifications(TeacherRequiredMixin,View):
    template_name = 'teacher/list_notifications.html'

    def get(self, request):
        notifications = Notification.objects.filter(sender=request.user.teacher)
        return render(request, self.template_name, {'notifications': notifications})

class UpdateNotification(TeacherRequiredMixin,View):
    template_name = 'teacher/update_notification.html'

    def get(self, request, notification_id):
        notification = Notification.objects.get(pk=notification_id)
        form = NotificationForm(instance=notification)
        return render(request, self.template_name, {'form': form})

    def post(self, request, notification_id):
        notification = Notification.objects.get(pk=notification_id)
        form = NotificationForm(request.POST, instance=notification)
        if form.is_valid():
            form.instance.sender = request.user.teacher
            form.save()
            return redirect('list_notification')
        return render(request, self.template_name, {'form': form})

class DeleteNotification(TeacherRequiredMixin,View):
    template_name = 'teacher/delete_notification.html'

    def get(self, request, notification_id):
        notification = Notification.objects.get(pk=notification_id)
        context = {'notification': notification}
        return render(request, self.template_name, context)

    def post(self, request, notification_id):
        notification = Notification.objects.get(pk=notification_id)
        notification.delete()
        return redirect('list_notification')

# Teacher Profile

class TeacherProfileView(TeacherRequiredMixin,DetailView):
    def get(self, request):
        teacher = request.user.teacher
        return render(request, 'teacher/teacher_profile.html', {'teacher': teacher})

# Room List

class RoomList(TeacherRequiredMixin,ListView):

    def get(self, request):
        rooms = Room.objects.all()
        context = {
            'rooms' : rooms,
        }
        return render(request, 'teacher/rooms.html', context)

class RoomView(TeacherRequiredMixin,DetailView):
    model = Room
    template_name = 'teacher/room.html'
    context_object_name = 'room'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = self.object
        messages = Message.objects.filter(room=room)
        context['messages'] = messages
        return context

