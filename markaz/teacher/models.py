from django.db import models
from principle.models import *
from django.utils import timezone
# Create your models here.

class StudyMaterial(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    file = models.FileField(upload_to='study_materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
        

class TeacherAttendance(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    morning_attendance = models.BooleanField(default=False)
    afternoon_attendance = models.BooleanField(default=False)

    class Meta:
        unique_together = ('teacher', 'date')


    def __str__(self):
        return f"{self.teacher.name}'s Attendance on {self.date}"

    

class Notification(models.Model):
    sender = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    scheduled_at = models.DateTimeField()



    def __str__(self):
        return f"Notification from {self.sender.name} to {self.recipient.name}"


