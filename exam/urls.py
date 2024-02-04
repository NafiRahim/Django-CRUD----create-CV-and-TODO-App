"""
URL configuration for exam project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from CV_generator import views as cv_views
from Scheduler import views as sch_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', cv_views.home, name='home'),
    path('cv/', cv_views.create_cv, name='cv'),
    path('view/', cv_views.view, name='view'),

    # path('down/<int:id>/', cv_views.download_cv, name='download_cv'),
    path('cv/pdf/<int:cv_id>/', cv_views.generate_cv_pdf, name='cv_pdf'),

    path('scheduler/', sch_views.add_task, name='add_task'),
    path('task_list/', sch_views.ToDo, name='task_list'),
    path('edit_task/<int:task_id>/', sch_views.edit_task, name='edit_task'),
    path('update-task-status/<int:task_id>/', sch_views.update_task_status, name='update_task_status'),
    path('delete_task/<int:task_id>/', sch_views.delete_task, name='delete_task'),






]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)