from import_export import resources
from principle.models import *
from teacher.models import *

class StudentResource(resources.ModelResource):
    class Meta:
        model = Student

class TeacherResource(resources.ModelResource):
    class Meta:
        model = Teacher

# class TeacherAttendanceResource(resources.ModelResource):
#     class Meta:
#         model = Attendance

class AcademicDetailResource(resources.ModelResource):
    class Meta:
        model = AcademicDetail