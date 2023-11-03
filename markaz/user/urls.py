from django.urls import path
from user import views


urlpatterns = [
    path('', views.checkpath),
    path('login/', views.custom_login, name='custom_login'),
    path('otp_verification/', views.otp_verification_view, name='otp_verification'),

]
