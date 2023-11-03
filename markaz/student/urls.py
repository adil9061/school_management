from django.urls import path
from student import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('student_home', views.StudentHome.as_view(), name="student_home"),
    path('logout/', LogoutView.as_view(), name='logout'),

    # View Study Material

    path('materials_list/', views.MaterialsList.as_view(), name="materials_list"),

    path('view_materials/<int:material_id>/', views.ViewMaterials.as_view(), name='view_materials'),

    # View Academic Detail

    path('student_academic_detail/', views.StudentAcademicDetailView.as_view(), name='student_academic_detail'),

    # Download

    path('certificate/<int:certificate_id>/download/', views.DownloadCertificateView.as_view(), name='download_certificate'),
    
    path('certificate/', views.CertificateListView.as_view(), name='certificate'),

    path('student_academic_detail_pdf/', views.StudentAcademicDetailPdfView.as_view(), name='academic_detail_pdf'),

    # View Announcment

    path('student_announcement/', views.StudentAnnouncements.as_view(), name='student_announcements'),

    # View Notification

    path('see_notification/', views.SeeNotificationView.as_view(), name='see_notification'),

    # View Rooms

    path('student/rooms/', views.StudentRooms.as_view(), name='student_rooms'),

    path('<slug:slug>/', views.RoomView.as_view(), name='room'),

    # View Video Study Materials

    path('student/video_library/', views.VideoLibrary.as_view(), name='video_librarys'),

    # For Student Profile

    path('student/profile/', views.StudentProfile.as_view(), name='student_profile'),
]
