from django.shortcuts import render, redirect
from .models import Task
# Create your views here.

from django.shortcuts import render, redirect
from .models import Task

def ToDo(request):
    tasks = Task.objects.all()
    return render(request, 'Scheduler/scheduler.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        task_name = request.POST.get('task_name')
        description = request.POST.get('description')
        is_finished = request.POST.get('is_finished', False)

        # Convert the string value to a boolean
        is_finished = is_finished == 'on'
        
        Task.objects.create(
            task_name=task_name,
            description=description,
            is_finished=is_finished
        )
    return render(request, 'Scheduler/add_task.html')

def edit_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        # Handle the case where the task does not exist
        return redirect('task_list')

    if request.method == 'POST':
        task.task_name = request.POST.get('task_name')
        task.description = request.POST.get('description')
        task.is_finished = request.POST.get('is_finished', False)

        # Convert the string value to a boolean
        task.is_finished = task.is_finished == 'on'
        
        task.save()
        return redirect('task_list')
    return render(request, 'Scheduler/edit_task.html', {'task': task})

def delete_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        # Handle the case where the task does not exist
        return redirect('task_list')

    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'Scheduler/delete_task.html', {'task': task})


def update_task_status(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(id=task_id)
        # Toggle the is_finished status
        task.is_finished = not task.is_finished
        task.save()
        return redirect('task_list')  # Redirect to the task list page