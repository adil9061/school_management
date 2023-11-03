from django import forms
from principle.models import *


class StudentRegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['user']

class TeacherRegisterForm(forms.ModelForm):

    class Meta:
        model = Teacher
        exclude = ['user']

class CoursesForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = '__all__'

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'

class AcademicDetailForm(forms.ModelForm):
    class Meta:
        model = AcademicDetail
        fields = ['student', 'exam', 'course', 'subject', 'individual_score']

class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['student', 'course']


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'show_to_teachers', 'show_to_students']

class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = '__all__'

class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = '__all__'


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = '__all__'

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
