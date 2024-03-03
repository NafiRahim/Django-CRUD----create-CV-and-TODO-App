from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.register, name='register'),
    path('otp-verify/', views.otp_verify, name='otp_verify'),
    # path('reset-password/', views.reset, name='reset'),
    # path('change-password/', views.update_pass, name='UpPass')
    path('change-password/', views.change_pass, name='change_pass'),
]