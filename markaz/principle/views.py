from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from principle.serializers import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from teacher.urls import *
from teacher.models import *
from student.urls import *
from principle.models import *
from django.contrib.auth.decorators import login_required
from principle.resources import *
import tablib
from django.contrib import messages
from django.contrib.auth import get_user_model
from principle.forms import *
import csv
from django.template.loader import get_template
import requests
import json
from markaz.settings import *
from django.views.generic.edit import CreateView
from django.views import View
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from principle.mixins import AdminRequiredMixin,admin_required
from user.models import *
from datetime import timedelta
from django.utils import timezone


# Admin Home
@method_decorator(login_required(login_url='custom_login'), name='dispatch')
class AdminHome(AdminRequiredMixin,View):
    def get(self, request):
        return render(request, 'principle/adminhome.html')

# For Permission Denied

def no_permission(request):
    return render(request, 'principle/no_permission.html')

# Add Country, State, City

class CountryCreateView(AdminRequiredMixin,View):
    def get(self,request):
        form = CountryForm()
        return render(request, 'principle/add_country.html', {'form' : form})
    
    def post(self,request):
        form = CountryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add-country')
        return render(request, 'principle/add_country.html', {'form' : form})

class StateCreateView(AdminRequiredMixin,View):
    def get(self,request):
        form = StateForm()
        return render(request, 'principle/add_state.html', {'form' : form})

    def post(self, request):
        form = StateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add-state')
        return render(request, 'principle/add_state.html', {'form' : form})

class CityCreateView(AdminRequiredMixin,View):
    def get(self,request):
        form = CityForm()
        return render(request, 'principle/add_city.html', {'form' : form})

    def post(self,request):
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add-city')
        return render(request, 'principle/add_city.html', {'form' : form})

# Load states and cities

class LoadStatesView(View):
    def get(self, request):
        country_id = request.GET.get('country_id')
        states = State.objects.filter(country_id=country_id)
        state_data = [{'id': state.id, 'name': state.name} for state in states]
        return JsonResponse({'states': state_data})

class LoadCitiesView(View):
    def get(self, request):
        state_id = request.GET.get('state_id')
        cities = City.objects.filter(state_id=state_id)
        city_data = [{'id': city.id, 'name': city.name} for city in cities]
        return JsonResponse({'cities': city_data})

# Country List, Update, Delete

class CountryList(AdminRequiredMixin,View):

    def get(self, request):
        country = Country.objects.all()
        context ={
            'country' : country,
        }
        return render(request, 'principle/country_list.html', context)

class UpdateCountry(AdminRequiredMixin,View):

    def get(self, request, country_id):
        country = get_object_or_404(Country, pk=country_id)
        form = CountryForm(instance=country)
        return render(request, 'principle/update_country.html', {'form' : form, 'country' : country})

    def post(self, request, country_id):
        country = get_object_or_404(Country, pk=country_id)
        form = CountryForm(request.POST, instance=country)
        if form.is_valid():
            form.save()
            return redirect('country_list')
        return render(request, 'principle/update_country.html', {'form' : form, 'country' : country})

class DeleteCountry(AdminRequiredMixin, View):
    def get(self, request, country_id):
        country = get_object_or_404(Country, pk=country_id)
        return render(request, 'principle/delete_country.html', {'country' : country})

    def post(self, request, country_id):
        country = get_object_or_404(Country, pk=country_id)
        related_models = [State, City, Teacher, Student]
        for related_model in related_models:
            related_objects = related_model.objects.filter(country=country)
            related_objects.delete()

        country.delete()
        return redirect('country_list')

# State List, Update, Delete

class StateList(AdminRequiredMixin,View):

    def get(self, request):
        state = State.objects.all()
        context = {
            'state' : state,
        }
        return render(request, 'principle/state_list.html', context)

class UpdateState(AdminRequiredMixin, View):

    def get(self, request, state_id):
        state = get_object_or_404(State, pk=state_id)
        form = StateForm(instance=state)
        return render(request, 'principle/update_state.html', {'form' : form, 'state' : state})

    def post(self, request, state_id):
        state = get_object_or_404(State, pk=state_id)
        form = StateForm(request.POST, instance=state)
        if form.is_valid():
            form.save()
            return redirect('state_list')
        return render(request, 'principle/update_state.html', {'form' : form, 'state' : state})

class DeleteState(AdminRequiredMixin, View):
    def get(self, request, state_id):
        state = get_object_or_404(State, pk=state_id)
        return render(request, 'principle/delete_state.html', {'state' : state})

    def post(self, request, state_id):
        state = get_object_or_404(State, pk=state_id)
        related_models = [City, Teacher, Student]
        for related_model in related_models:
            related_objects = related_model.objects.filter(state=state)
            related_objects.delete()

        state.delete()
        return redirect('state_list')

# City List, Update, Delete

class CityList(AdminRequiredMixin,View):

    def get(self, request):
        city = City.objects.all()
        context = {
            'city' : city,
        }
        return render(request, 'principle/city_list.html', context)

class UpdateCity(AdminRequiredMixin, View):

    def get(self, request, city_id):
        city = get_object_or_404(City, pk=city_id)
        form = CityForm(instance=city)
        return render(request, 'principle/update_city.html', {'form' : form, 'city' : city})

    def post(self, request, city_id):
        city = get_object_or_404(City, pk=city_id)
        form = CityForm(request.POST, instance=city)
        if form.is_valid():
            form.save()
            return redirect('city_list')
        return render(request, 'principle/update_city.html', {'form' : form, 'city' : city})

class DeleteCity(AdminRequiredMixin, View):
    def get(self, request, city_id):
        city = get_object_or_404(City, pk=city_id)
        return render(request, 'principle/delete_city.html', {'city' : city})

    def post(self, request, city_id):
        city = get_object_or_404(City, pk=city_id)
        related_models = [Teacher, Student]
        for related_model in related_models:
            related_objects = related_model.objects.filter(city=city)
            related_objects.delete()

        city.delete()
        return redirect('city_list')

# Registration of Teacher

@admin_required
def register_teacher(request):
    if request.method == 'POST':
        form = TeacherRegisterForm(request.POST)
        Username = request.POST['username']
        Password = request.POST['password']
        Email = request.POST['email']
        Reg_Id = request.POST['reg_id']
        Name = request.POST['name']
        Contact = request.POST['contact']
        Country_ad = request.POST['country']
        State_ad = request.POST['state']
        city_ad = request.POST['city']
        recaptcha_token = request.POST['token']


        data = {
            'secret' : RECAPTCHA_PRIVATE_KEY,
            'response' : recaptcha_token
        }

        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data = data)
        result = response.json()

        if result['success']:

            user = CustomUser(username=Username, password=Password, email=Email, is_teacher = True)
            user.save()
            country = Country.objects.get(pk = Country_ad)
            state = State.objects.get(pk = State_ad)
            city = City.objects.get(pk = city_ad)

            teacher = Teacher(user=user, reg_id=Reg_Id, name=Name, contact=Contact, country=country, state=state, city=city)
            teacher.save()
            return redirect('admin-home')
        else:
            pass
    else:
        form = TeacherRegisterForm()

    return render(request, 'principle/register_teacher.html', {'form' : form})


# Registration of Student

@admin_required
def register_student(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        Username = request.POST['username']
        Password = request.POST['password']
        Email = request.POST['email']
        Reg_Id = request.POST['reg_id']
        Name = request.POST['name']
        Contact = request.POST['contact']
        Course = request.POST['course']
        Country_ad = request.POST['country']
        State_ad = request.POST['state']
        city_ad = request.POST['city']
        Start_year = request.POST['start_year']
        End_year = request.POST['end_year']
        recaptcha_token = request.POST['token']

        data = {
            'secret' : RECAPTCHA_PRIVATE_KEY,
            'response' : recaptcha_token
        }

        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data = data)
        result = response.json()

        if result['success']:

            user = CustomUser(username=Username, password=Password, email=Email, is_student= True)
            user.save()
            course = Courses.objects.get(pk = Course)
            country = Country.objects.get(pk = Country_ad)
            state = State.objects.get(pk = State_ad)
            city = City.objects.get(pk = city_ad)
            student = Student(user=user, reg_id=Reg_Id, name=Name, contact=Contact, course=course, country=country, state=state, city=city, start_year=Start_year, end_year=End_year)
            student.save()
            return redirect('admin-home')
        else:
            pass
    else:
        form = StudentRegisterForm()
    
    return render(request, 'principle/register_student.html', {'form' : form})

# List of Student and Teacher

class StudentListView(AdminRequiredMixin,View):
    def get(self, request):
        students = Student.objects.filter(user__is_active=True)
        context = {
            'students': students,
        }
        return render(request, 'principle/student_list.html', context)

class TeacherListView(AdminRequiredMixin,View):
    def get(self, request):
        teachers = Teacher.objects.filter(user__is_active=True)
        context = {
            'teachers' : teachers,
        }
        return render(request, 'principle/teacher_list.html', context)

# Update and Delete for Student

class UpdateStudent(AdminRequiredMixin,View):

    def get(self, request, student_id):
        student = get_object_or_404(Student, pk=student_id)
        form = StudentRegisterForm(instance=student)
        return render(request, 'principle/update_student.html', {'form': form, 'student': student})

    def post(self, request, student_id):
        student = get_object_or_404(Student, pk=student_id)
        form = StudentRegisterForm(request.POST, instance=student)
        if form.is_valid():
            reg_id = form.cleaned_data['reg_id']
            existing_student = Student.objects.exclude(pk=student_id).filter(reg_id=reg_id)
        
            if existing_student.exists():
                form.add_error('reg_id', 'Registration ID is already taken.')
            else:
                form.save()
                return redirect('list_student')
        return render(request, 'principle/update_student.html', {'form': form, 'student': student})


class DeleteStudent(AdminRequiredMixin, View):

    def get(self, request, student_id):
        student = get_object_or_404(Student, pk=student_id)
        return render(request, 'principle/delete_student.html', {'student': student})

    def post(self, request, student_id):
        student = get_object_or_404(Student, pk=student_id)
        user = student.user
        user.is_active = False
        user.save()

        return redirect('list_student')

# Update and Delete for Teacher

class UpdateTeacher(AdminRequiredMixin,View):

    def get(self, request, teacher_id):
        teacher = get_object_or_404(Teacher, pk=teacher_id)
        form = TeacherRegisterForm(instance=teacher)
        return render(request, 'principle/update_teacher.html', {'form' : form, 'teacher' : teacher})

    def post(self, request, teacher_id):
        teacher = get_object_or_404(Teacher, pk=teacher_id)
        form = TeacherRegisterForm(request.POST, instance=teacher)
        if form.is_valid():
            reg_id = form.cleaned_data['reg_id']
            existing_teacher = Teacher.objects.exclude(pk=teacher_id).filter(reg_id=reg_id)
        
            if existing_teacher.exists():
                form.add_error('reg_id', 'Registration ID is already taken.')
            else:
                form.save()
                return redirect('list_teacher')
        return render(request, 'principle/update_teacher.html', {'form' : form, 'teacher' : teacher})

class DeleteTeacher(AdminRequiredMixin, View):

    def get(self, request, teacher_id):
        teacher = get_object_or_404(Teacher, pk=teacher_id)
        return render(request, 'principle/delete_teacher.html', {'teacher': teacher})

    def post(self, request, teacher_id):
        teacher = get_object_or_404(Teacher, pk=teacher_id)
        user = teacher.user
        user.is_active = False
        user.save()

        return redirect('list_teacher')

# Student CRUD

@api_view(['GET'])
def studentlist(request):
    student = Student.objects.all()
    serializer = StudentRegistrationSerializer(student, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def createstudent(request):

    data = request.data

    Username = data.get('username')
    Password = data.get('password')
    Email = data.get('email')
    Reg_id = data.get('reg_id')
    Name = data.get('name')
    Contact = data.get('contact')
    Course = data.get('course')
    Country_ad = data.get('country')
    State_ad = data.get('state')
    city_ad = data.get('city')
    Start_year = data.get('start_year')
    End_year = data.get('end_year')

    user = CustomUserSerializer(data = { "username" : Username, "password" : Password, "email" : Email})

    if user.is_valid():
        student_user = user.save()
    else:
        return Response({'error' : 'invalid user data'}, status=400)
    
    student = StudentRegistrationSerializer(data={
        'user' : student_user.id,
        "reg_id" : Reg_id,
        "name" : Name,
        "contact": Contact,
        "course" : Course,
        "country" : Country_ad,
        "state" : State_ad,
        "city" : city_ad,
        "start_year" : Start_year,
        "end_year" : End_year
    })

    if student.is_valid():
        student.save()
        return Response('New student created..')
    else:
        student_user.delete()
        return Response({'error' : 'Invalid profile data'}, status=400)

@api_view(['PUT'])
def studentupdate(request, id):
    student = Student.objects.get(pk = id)
    serializers = StudentRegistrationSerializer(student, data=request.data)
    if serializers.is_valid():
        serializers.save()
        return Response('Student detail updated')
    else:
        return Response("Can't save")
    return Response(serializers.data)

@api_view(['DELETE'])
def deletestudent(request, id):
    student = Student.objects.get(pk = id)
    student_user = student.user.id
    user = CustomUser.objects.get(pk = student_user)
    student.delete()
    user.delete()
    return Response('Deleted Successfully..')


# Teacher CRUD 

@api_view(['GET'])
def teacherlist(request):
    teacher = Teacher.objects.all()
    serializers = TeacherRegistrationSerializer(teacher, many=True)
    return Response(serializers.data)

@api_view(['POST'])
def createteacher(request):

    data = request.data

    Username = data.get('username')
    Password = data.get('password')
    Email = data.get('email')
    Reg_id = data.get('reg_id')
    Name = data.get('name')
    Contact = data.get('contact')
    Country_ad = data.get('country')
    State_ad = data.get('state')
    city_ad = data.get('city')
    
    
    user = CustomUserSerializer(data = { "username" : Username, "password" : Password, "email" : Email})

    if user.is_valid():
        teacher_user = user.save()
    else:
        return Response({'error' : 'invalid user data'}, status=400)
    
    teacher = TeacherRegistrationSerializer(data={
        'user' : teacher_user.id,
        "reg_id" : Reg_id,
        "name" : Name,
        "contact" : Contact,
        "country" : Country_ad,
        "state" : State_ad,
        "city" : city_ad
    })

    if teacher.is_valid():
        teacher.save()
        return Response('New teacher created..')
    else:
        teacher_user.delete()
        return Response({'error' : 'Invalid profile data'}, status=400)

@api_view(['PUT'])
def teacherupdate(request, id):
    teacher = Teacher.objects.get(pk = id)
    serializers = TeacherRegistrationSerializer(teacher, data=request.data)
    if serializers.is_valid():
        serializers.save()
        return Response('Teacher detail updated')
    else:
        return Response("can't save")
    return Response(serializers.data)


@api_view(['DELETE'])
def deleteteacher(request, id):
    teacher = Teacher.objects.get(pk = id)
    teacher_user = teacher.user.id
    user = CustomUser.objects.get(pk = teacher_user)
    teacher.delete()
    user.delete()
    return Response('Deleted Successfully...')


# Export - Import Student Details

class ExportStudentsView(AdminRequiredMixin,View):

    def get(self, request):
        student_resource = Student.objects.all()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="student.csv"'

        writer = csv.writer(response)

        writer.writerow(['User', 'Reg_id', 'Name', 'Contact', 'Course', 'Country', 'State', 'City', 'Start_year', 'End_year'])

        for record in student_resource:
            writer.writerow([
                record.user.id,
                record.reg_id,
                record.name,
                record.contact,
                record.course,
                record.country,
                record.state,
                record.city,
                record.start_year,
                record.end_year,
            ])

        return response

# def import_students(request):
#     if request.method == 'POST':
#         student_resource = StudentResource()
#         dataset = tablib.Dataset()
#         new_students = request.FILES['myfile']

#         if not new_students.name.endswith('csv'):
#             messages.error(request, 'Please upload a CSV file..')
#         else:
#             imported_data = dataset.load(new_students.read().decode('utf-8'), format='csv')
#             CustomUser = get_user_model()
#             for data in imported_data:
#                 user = request.user
#                 student = Student(user=user, reg_id=data[0], name=data[1], course=data[2], batch=data[3])
#                 student.save()
#             messages.success(request, 'Students have been imported successfully..' )
#     return render(request, 'principle/import_students.html')


# Export of Teacher

class ExportTeachersView(AdminRequiredMixin,View):

    def get(self, request):
        teacher_resource = Teacher.objects.all()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="teacher.csv"'

        writer = csv.writer(response)

        writer.writerow(['User', 'Reg_id', 'Name', 'Contact', 'Country', 'State', 'City'])

        for record in teacher_resource:
            writer.writerow([
                record.user.id,
                record.reg_id,
                record.name,
                record.contact,
                record.country,
                record.state,
                record.city,
            ])

        return response

# Creating Course


class CreateCourseView(AdminRequiredMixin,View):

    def get(self, request):
        form = CoursesForm()
        return render(request, 'principle/create_course.html', {'form': form})

    def post(self, request):
        form = CoursesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-home')
        return render(request, 'principle/create_course.html', {'form': form})

# List, Update, Delete Course

class CourseList(AdminRequiredMixin, View):

    def get(self, request):
        courses = Courses.objects.all()
        context = {
            'courses' : courses,
        }
        return render(request, 'principle/course_list.html', context)

class UpdateCourse(AdminRequiredMixin,View):

    def get(self, request, course_id):
        course = get_object_or_404(Courses, pk=course_id)
        form = CoursesForm(instance=course)
        return render(request, 'principle/update_course.html', {'form': form, 'course': course})

    def post(self, request, course_id):
        course = get_object_or_404(Courses, pk=course_id)
        form = CoursesForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')
        return render(request, 'principle/update_course.html', {'form': form, 'course': course})

class DeleteCourse(AdminRequiredMixin, View):
    def get(self, request, course_id):
        course = get_object_or_404(Courses, pk=course_id)
        return render(request, 'principle/delete_course.html', {'course': course})

    def post(self, request, course_id):
        course = get_object_or_404(Courses, pk=course_id)
        related_models = [Student,Subject,AcademicDetail,Certificate,Room]
        for related_model in related_models:
            related_objects = related_model.objects.filter(course=course)
            related_objects.delete()

        course.delete()
        return redirect('course_list')

# Create Exam

class CreateExamView(AdminRequiredMixin,View):

    def get(self, request):
        form = ExamForm()
        return render(request, 'principle/add_exam.html', {'form' : form})

    def post(self, request):
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-home')
        return render(request, 'principle/add_exam.html', {'form' : form})

# List, Update, Delete Exam

class ExamList(AdminRequiredMixin, View):

    def get(self, request):
        exams = Exam.objects.all()
        context = {
            'exams' : exams,
        }
        return render(request, 'principle/exam_list.html', context)

class UpdateExam(AdminRequiredMixin,View):

    def get(self, request, exam_id):
        exam = get_object_or_404(Exam, pk=exam_id)
        form = ExamForm(instance=exam)
        return render(request, 'principle/update_exam.html', {'form': form, 'exam': exam})

    def post(self, request, exam_id):
        exam = get_object_or_404(Exam, pk=exam_id)
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            return redirect('exam_list')
        return render(request, 'principle/update_exam.html', {'form': form, 'exam': exam})

class DeleteExam(AdminRequiredMixin, View):
    def get(self, request, exam_id):
        exam = get_object_or_404(Exam, pk=exam_id)
        return render(request, 'principle/delete_exam.html', {'exam' : exam})

    def post(self, request, exam_id):
        exam = get_object_or_404(Exam, pk=exam_id)
        related_models = [Subject,AcademicDetail]
        for related_model in related_models:
            related_objects = related_model.objects.filter(exam=exam)
            related_objects.delete()

        exam.delete()
        return redirect('exam_list')

# Create Subject

class CreateSubjectView(AdminRequiredMixin,View):

    def get(self, request):
        form = SubjectForm()
        return render(request, 'principle/add_subject.html', {'form' : form})

    def post(self, request):
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-home')
        return render(request, 'principle/add_subject.html', {'form' : form})
        
# List, Update, Delete Subject

class SubjectList(AdminRequiredMixin, View):

    def get(self, request):
        subjects = Subject.objects.all()
        context = {
            'subjects' : subjects,
        }
        return render(request, 'principle/subject_list.html', context)

class UpdateSubject(AdminRequiredMixin,View):

    def get(self, request, subject_id):
        subject = get_object_or_404(Subject, pk=subject_id)
        form = SubjectForm(instance=subject)
        return render(request, 'principle/update_subject.html', {'form': form, 'subject': subject})

    def post(self, request, subject_id):
        subject = get_object_or_404(Subject, pk=subject_id)
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('subject_list')
        return render(request, 'principle/update_subject.html', {'form': form, 'subject': subject})

class DeleteSubject(AdminRequiredMixin, View):
    def get(self, request, subject_id):
        subject = get_object_or_404(Subject, pk=subject_id)
        return render(request, 'principle/delete_subject.html', {'subject' : subject})

    def post(self, request, subject_id):
        subject = get_object_or_404(Subject, pk=subject_id)
        related_models = [AcademicDetail]
        for related_model in related_models:
            related_objects = related_model.objects.filter(subject=subject)
            related_objects.delete()

        subject.delete()
        return redirect('subject_list')

# Add Student Academic Details

class AddAcademicDetail(AdminRequiredMixin,View):

    def get(self, request):
        form = AcademicDetailForm()
        return render(request, 'principle/add_academic_detail.html', {'form': form})

    def post(self, request):
        form = AcademicDetailForm(request.POST)
        if form.is_valid():
            academic_detail = form.save(commit=False)

            if academic_detail.individual_score >= 90:
                academic_detail.grade = 'A'
            elif academic_detail.individual_score >= 76:
                academic_detail.grade = 'B'
            elif academic_detail.individual_score >= 57:
                academic_detail.grade = 'C'
            elif academic_detail.individual_score >= 40:
                academic_detail.grade = 'D'
            else:
                academic_detail.grade = 'F'

            academic_detail.save()
            return redirect('admin-home')
        return render(request, 'principle/add_academic_detail.html', {'form': form})

class AcademicDetailView(AdminRequiredMixin,View):

    def get(self, request, student_id):
        student = Student.objects.get(pk=student_id)
        academic_details = AcademicDetail.objects.filter(student=student)

        grouped_academic_details = {}
        current_exam = None
        current_course = None
        details_list = []

        for detail in academic_details:
            if current_exam != detail.exam or current_course != detail.course:
                if current_exam is not None and current_course is not None:
                    grouped_academic_details[(current_exam, current_course)] = {
                        'rowspan': len(details_list),
                        'details': details_list,
                        'total_score': sum(detail.individual_score for detail in details_list),
                        'overall_grade': self.calculate_overall_grade(details_list),
                    }

                current_exam = detail.exam
                current_course = detail.course
                details_list = []

            details_list.append(detail)

        if current_exam is not None and current_course is not None:
            grouped_academic_details[(current_exam, current_course)] = {
                'rowspan': len(details_list),
                'details': details_list,
                'total_score': sum(detail.individual_score for detail in details_list),
                'overall_grade': self.calculate_overall_grade(details_list),
            }

        context = {
            'student': student,
            'academic_details': academic_details,
            'grouped_academic_details': grouped_academic_details,
        }

        return render(request, 'principle/academic_detail_view.html', context)

    def calculate_overall_grade(self, details_list):
        total_score = sum(detail.individual_score for detail in details_list)

        if total_score >= 520:
            return 'A'
        elif total_score >= 400:
            return 'B'
        elif total_score >= 320:
            return 'C'
        elif total_score >= 240:
            return 'D'
        else:
            return 'F'

class StudentList(AdminRequiredMixin,ListView):

    def get(self, request):
        students = Student.objects.all()
        context = {
            'students': students,
        }
        return render(request, 'principle/student_list1.html', context)

class ExportAcademicDetail(AdminRequiredMixin,View):

    def get(self, request):
        academic_detail_resource = AcademicDetailResource()
        dataset = academic_detail_resource.export()
        
        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="academic_detail.csv"'
        return response


# Teacher Attendace View For Admin

class ViewTeacherAttendance(AdminRequiredMixin,ListView):

    def get(self, request):
        teacher_attendance_records = TeacherAttendance.objects.all()
        context = {
            'teacher_attendance_records' : teacher_attendance_records,
        }
        return render(request, 'principle/view_teacher_attendance.html', context)

class ExportTeacherAttendance(AdminRequiredMixin,View):

    def get(self, request):
        teacher_attendance_records = TeacherAttendance.objects.all()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="teacher_attendance.csv"'

        writer = csv.writer(response)

        writer.writerow(['Teacher', 'Date', 'Morning Attendance', 'Afternoon Attendance'])

        for record in teacher_attendance_records:
            writer.writerow([
                f"{record.teacher.name}",
                str(record.date),
                "Present" if record.morning_attendance else "Absent",
                "Present" if record.afternoon_attendance else "Absent",
            ])

        return response

# Student Course Completion Generate


class CreateCertificate(AdminRequiredMixin,View):
    def get(self, request):
        form = CertificateForm
        return render(request, 'principle/create_certificate.html', {'form' : form})

    def post(self, request):
        form = CertificateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-home')
        return render(request, 'principle/create_certificate.html', {'form' : form})

class GenerateCertificate(AdminRequiredMixin,View):
    def get(self, request, pk):
        certificate = Certificate.objects.get(pk=pk)
        context = {
            'certificate' : certificate,
        }
        return render(request, 'principle/certificate_template.html', context)

class CertificateList(AdminRequiredMixin,ListView):

    def get(self, request):
        certificates = Certificate.objects.all()
        context = {
            'certificates' : certificates,
        }
        return render(request, 'principle/certificate_list.html', context)

# For Creating announcements for Teacher and Student

class CreateAnnouncement(View):

    def get(self, request):
        form = AnnouncementForm()
        return render(request, 'principle/create_announcement.html', {'form': form})

    def post(self, request):
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.user = request.user
            announcement.save()
            return redirect('admin-home')
        return render(request, 'principle/create_announcement.html', {'form': form})
    
class AnnouncementsList(View):

    def get(self, request):
        expired_at = timezone.now() - timedelta(days=1)
        Announcement.objects.filter(created_at__lte=expired_at).delete()
        announcements = Announcement.objects.all()
        return render(request, 'principle/announcements_list.html', {'announcements': announcements})

# For Announcement Update and Delete

class UpdateAnnouncement(View):

    def get(self, request, announcement_id):
        announcement = get_object_or_404(Announcement, pk=announcement_id)
        form = AnnouncementForm(instance=announcement)
        return render(request, 'principle/update_announcement.html', {'form': form, 'announcement': announcement})

    def post(self, request, announcement_id):
        announcement = get_object_or_404(Announcement, pk=announcement_id)
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('announcement_list')
        return render(request, 'principle/update_announcement.html', {'form': form, 'announcement': announcement})

class DeleteAnnouncement(View):

    def get(self, request, announcement_id):
        announcement = get_object_or_404(Announcement, pk=announcement_id)
        return render(request, 'principle/delete_announcement.html', {'announcement': announcement})

    def post(self, request, announcement_id):
        announcement = get_object_or_404(Announcement, pk=announcement_id)
        announcement.delete()
        return redirect('announcement_list')

# Room List

class CreateRoom(AdminRequiredMixin,View):
    def get(self,request):
        form = RoomForm()
        return render(request, 'principle/add_room.html', {'form' : form})

    def post(self,request):
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-home')
        return render(request, 'principle/add_room.html', {'form' : form})

class AdminRoom(AdminRequiredMixin,View):

    def get(self, request):
        rooms = Room.objects.all()
        context = {
            'rooms' : rooms,
        }
        return render(request, 'principle/rooms.html', context)

class RoomView(AdminRequiredMixin,DetailView):
    model = Room
    template_name = 'principle/room.html'
    context_object_name = 'room'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = self.object
        messages = Message.objects.filter(room=room)
        context['messages'] = messages
        return context

# List of Deleted Student and Teacher

class DeletedTeacherList(AdminRequiredMixin,View):
    def get(self, request):
        teachers = Teacher.objects.filter(user__is_active=False)
        context = {
            'teachers' : teachers,
        }
        return render(request, 'principle/deleted_teacher_list.html', context)

class DeletedStudentList(AdminRequiredMixin,View):
    def get(self, request):
        students = Student.objects.filter(user__is_active=False)
        context = {
            'students' : students,
        }
        return render(request, 'principle/deleted_student_list.html', context)
