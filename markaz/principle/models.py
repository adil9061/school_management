from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from user.models import CustomUser
# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class State(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    reg_id = models.CharField(max_length=50,default="TR", unique=True)
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)


    def __str__(self):
        return self.name
    

class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    course_fee = models.CharField(max_length=100)

    def __str__(self):
        return self.course_name
    

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    reg_id = models.CharField(max_length=50, default="STD", unique=True)
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    course = models.ForeignKey(Courses, on_delete= models.DO_NOTHING)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    start_year = models.DateField()
    end_year = models.DateField()

    
    def __str__(self):
        return self.name


class Exam(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Subject(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name
    
class AcademicDetail(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    individual_score = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=2)
    total_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    overall_grade = models.CharField(max_length=2, blank=True, null=True)

    def __str__(self):
        return f"{self.student.name}'s {self.subject} Score"
        
class Certificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)


    def __str__(self):
        return f"Certificate for {self.student.name} - {self.course.course_name}"

CustomUser = get_user_model()

class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    show_to_teachers = models.BooleanField(default=False, verbose_name="Show to Teachers")
    show_to_students = models.BooleanField(default=False, verbose_name="Show to Students")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


    def __str__(self):
        return self.title
    
class Room(models.Model):
    name = models.CharField(max_length=250)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)

    def __str__(self):
        return self.user


    