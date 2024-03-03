from django.urls import path
from . import views

urlpatterns = [
    path('add_task/', views.add_task, name='add_task'),
    path('task_list/', views.ToDo, name='task_list'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('update-task-status/<int:task_id>/', views.update_task_status, name='update_task_status'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
]