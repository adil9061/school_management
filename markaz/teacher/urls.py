from django.urls import path
from teacher import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('teacher_home/', views.TeacherHomeView.as_view(), name='teacher_home'),
    
    path('logout/', LogoutView.as_view(), name='logout'),

    # Add Study Material

    path('add_study_material/', views.AddStudyMaterialView.as_view(), name='add_study_material'),

    # Study Material List, View, Update, Delete

    path('uploded_materials/', views.UploadedStudyMaterialList.as_view(), name='uploded_materials'),

    path('view_materials/<int:material_id>/', views.ViewMaterials.as_view(), name='view_materials_teacher'),

    path('update_materials/<int:material_id>/', views.UpdateStudyMaterial.as_view(), name='update_studymaterial'),

    path('delete_study_material/<int:material_id>/', views.DeleteStudyMaterial.as_view(), name='delete_study_material'),

    # Mark Attendance
    
    path('mark_attendance/', views.MarkAttendance.as_view(), name='mark_attendance'),

    # View Announcement

    path('teacher_announcements/', views.TeacherAnnouncements.as_view(), name='teacher_announcements'),

    # Send Notification

    path('send_notification/', views.SendNotification.as_view(), name='send_notification'),

    # Notification List, Update, Delete

    path('notification_list/', views.ListNotifications.as_view(), name='list_notification'),
    path('update-notification/<int:notification_id>/', views.UpdateNotification.as_view(), name='update_notification'),
    path('delete_notification/<int:notification_id>/', views.DeleteNotification.as_view(), name='delete_notification'),


    # Teacher Profile

    path('teacher/profile/', views.TeacherProfileView.as_view() ,name='teacher_profile'),

    # Chat Room

    path('rooms/', views.RoomList.as_view(), name='teacher_rooms'),

    path('<slug:slug>/', views.RoomView.as_view(), name='teacher_room'),

    ]