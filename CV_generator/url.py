from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('cv/', views.create_cv, name='cv'),
    path('view/', views.view, name='view'),
    path('cv/pdf/<int:cv_id>/', views.generate_cv_pdf, name='cv_pdf'),
]