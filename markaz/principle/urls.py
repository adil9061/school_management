from django.urls import path
from principle import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # path('', views.checkpath),
    path('no_permission/', views.no_permission, name='no_permission'),

    # Register teacher and student

    path('register/teacher/', views.register_teacher, name='teacher-registration'),
    path('register/student/', views.register_student, name='student-registration'),

    # Add country, state, city

    path('add-country/', views.CountryCreateView.as_view(), name='add-country'),

    path('add-state/', views.StateCreateView.as_view(), name='add-state'),

    path('add-city/', views.CityCreateView.as_view(), name='add-city'),

    # Load state and city

    path('load_states/', views.LoadStatesView.as_view(), name='load_states'),
    path('load_cities/', views.LoadCitiesView.as_view(), name='load_cities'),

    # Country List, Update

    path('country_list/', views.CountryList.as_view(), name='country_list'),
    path('update_country/<int:country_id>/', views.UpdateCountry.as_view(), name='update_country'),
    path('delete_country/<int:country_id>/', views.DeleteCountry.as_view(), name='delete_country'),

    # State List, Update

    path('state_list/', views.StateList.as_view(), name='state_list'),
    path('update_state/<int:state_id>/', views.UpdateState.as_view(), name='update_state'),
    path('delete_state/<int:state_id>/', views.DeleteState.as_view(), name='delete_state'),

    # City List, Update

    path('city_list/', views.CityList.as_view(), name='city_list'),
    path('update_city/<int:city_id>/', views.UpdateCity.as_view(), name='update_city'),
    path('delete_city/<int:city_id>/', views.DeleteCity.as_view(), name='delete_city'),

    # For Logout

    path('logout/', LogoutView.as_view(), name='logout'),
    
    # For Admin Home

    path('admin-home', views.AdminHome.as_view(), name='admin-home'),

    # List Student and Teacher

    path('list_student/', views.StudentListView.as_view(), name='list_student'),
    path('list_teacher/', views.TeacherListView.as_view(), name='list_teacher'),

    # Update and Delete Student

    path('update_student/<int:student_id>/', views.UpdateStudent.as_view(), name='update_student'),
    path('student/delete/<int:student_id>/', views.DeleteStudent.as_view(), name='delete_student'),

    # Update and Delete Teacher

    path('update_teacher/<int:teacher_id>/', views.UpdateTeacher.as_view(), name='update_teacher'),
    path('teacher/delete/<int:teacher_id>/', views.DeleteTeacher.as_view(), name='delete_teacher'),

    # List of Deleted Student and Teacher

    path('deleted_teacher_list/', views.DeletedTeacherList.as_view(), name='deleted_teacher_list'),
    path('deleted_student_list/', views.DeletedStudentList.as_view(), name='deleted_student_list'),


    # Export and Import teacher and student

    path('export-students/', views.ExportStudentsView.as_view(), name='export_students'),
    # path('import-students/', views.import_students, name='import_students'),
    path('export-teachers/', views.ExportTeachersView.as_view(), name='export_teachers'),


    # Student crud operation

    path('studentlist/', views.studentlist, name='studentlist'),
    path('createstudent/', views.createstudent, name='createstudent'),
    path('studentupdate/<int:id>', views.studentupdate, name='studentupdate'),
    path('deletestudent/<int:id>', views.deletestudent, name='deletestudent'),


    # Teacher crud operation

    path('teacherlist/', views.teacherlist, name='teacherlist'),
    path('createteacher/', views.createteacher, name='createteacher'),
    path('teacherupdate/<int:id>', views.teacherupdate, name='teacherupdate'),
    path('deleteteacher/<int:id>', views.deleteteacher, name='deleteteacher'),

    # path('otp_verification/', views.otp_verification_view, name='otp_verification'),

    # Student Grade Card

    path('create_course/', views.CreateCourseView.as_view(), name='create_course'),
    path('add-exam/', views.CreateExamView.as_view(), name='add-exam'),
    path('add-subject/', views.CreateSubjectView.as_view(), name='add-subject'),
    path('add-academic-detail/', views.AddAcademicDetail.as_view(), name='add-academic-detail'),
    path('students/', views.StudentList.as_view(), name='student-list'),
    path('students/<int:student_id>/', views.AcademicDetailView.as_view(), name='view-academic-details'),
    path('export-academic-detail/', views.ExportAcademicDetail.as_view(), name='export_academic_detail'),

    # Course list, update, delete

    path('course_list/', views.CourseList.as_view(), name='course_list'),
    path('update_course/<int:course_id>/', views.UpdateCourse.as_view(), name='update_course'),
    path('delete_course/<int:course_id>/', views.DeleteCourse.as_view(), name='delete_course'),
    # Exam list, update, delete

    path('exam_list/', views.ExamList.as_view(), name='exam_list'),
    path('update_exam/<int:exam_id>/', views.UpdateExam.as_view(), name='update_exam'),
    path('delete_exam/<int:exam_id>/', views.DeleteExam.as_view(), name='delete_exam'),

    # Subject list, update, delete

    path('subject_list/', views.SubjectList.as_view(), name='subject_list'),
    path('update_subject/<int:subject_id>/', views.UpdateSubject.as_view(), name='update_subject'),
    path('delete_subject/<int:subject_id>/', views.DeleteSubject.as_view(), name='delete_subject'),

    # Teacher Attendance View

    path('view-teacher-attendance/', views.ViewTeacherAttendance.as_view(), name='view_teacher_attendance'),
    path('export-teacher-attendance/', views.ExportTeacherAttendance.as_view(), name='export_teacher_attendance'),

    # Student Course Completion

    path('create/', views.CreateCertificate.as_view(), name='create_certificate'),
    path('generate/<int:pk>/', views.GenerateCertificate.as_view(), name='generate_certificate'),
    path('certificate/', views.CertificateList.as_view(), name='certificate_list'),

    # Creating Announcements

    path('create_announcement/', views.CreateAnnouncement.as_view(), name='create_announcement'),
    path('announcement_list/', views.AnnouncementsList.as_view(), name='announcement_list'),

    # Update and Delete Announcement

    path('update_announcement/<int:announcement_id>/', views.UpdateAnnouncement.as_view(), name='update_announcement'),
    path('delete_announcement/<int:announcement_id>/', views.DeleteAnnouncement.as_view(), name='delete_announcement'),


    # Chat Module

    path('add_room/', views.CreateRoom.as_view(), name='add_room'),
    path('rooms/', views.AdminRoom.as_view(), name='admin_rooms'),
    path('room/<int:room_id>/', views.RoomView.as_view(), name='admin_room'),
    
]
