from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'accounts/login.html')

def reset(request):
    return render(request, 'accounts/reset.html')

def register(request):
    return render(request, 'accounts/register.html')

def logout(request):
    return render(request, 'CV_generator/hello.html')