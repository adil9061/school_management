from rest_framework import serializers
from principle.models import *


class TeacherRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class StudentRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'email']