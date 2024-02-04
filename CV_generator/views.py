from django.shortcuts import render, redirect, HttpResponse, Http404
from .models import CV
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
# Create your views here.
def home(request):
    return render(request, 'CV_generator/hello.html')


def create_cv(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        about = request.POST.get('about')
        education = request.POST.get('education')
        experience = request.POST.get('experience')
        skills = request.POST.get('skills')
        interests = request.POST.get('interests')
        achievements = request.POST.get('achievements')
        references = request.POST.get('references')
        image = request.FILES.get('image')  # Assuming you have an image file field in your form

        # Create a new CV object
        cv = CV.objects.create(
            name=name,
            email=email,
            phone=phone,
            address=address,
            about=about,
            education=education,
            experience=experience,
            skills=skills,
            interests=interests,
            achievements=achievements,
            references=references,
            image=image
        )
  
    return render(request, 'CV_generator/create_cv.html')


def view(request):
    # Retrieve the CV object by its ID

    cv = CV.objects.all()

    return render(request, 'CV_generator/view_download.html', locals())




def generate_pdf(cv_id):
    try:
        cv = CV.objects.get(id=cv_id)
    except CV.DoesNotExist:
        # If the CV doesn't exist, return a message or handle it in your application's logic
        return HttpResponse("CV does not exist")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{cv.name}_CV.pdf"'

    # Create PDF
    pdf = canvas.Canvas(response, pagesize=letter)
    
    # Set up fonts
    pdf.setFont("Helvetica-Bold", 16)
    pdf.setFillColor(colors.black)

    # Add Title
    pdf.drawString(50, 750, 'Curriculum Vitae')
    pdf.drawString(50, 730, '------------------')

    # Add Image (at top right)
    if cv.image:
        img = ImageReader(cv.image.path)
        pdf.drawImage(img, 450, 700, width=100, height=100, mask='auto')

    # Add Personal Information
    y_offset = 650  # Initial y-coordinate for personal information
    personal_info = [
        f'Name: {cv.name}',
        f'Email: {cv.email}',
        f'Phone: {cv.phone}',
        f'Address: {cv.address}'
    ]
    for info in personal_info:
        pdf.drawString(50, y_offset, info)
        y_offset -= 20

    
    # Add About
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 590, 'About')
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, 570, f'{cv.about}')

    # Add Education
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 540, 'Education')
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, 520, f'{cv.education}')

    # Add Experience
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 490, 'Experience')
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, 470, f'{cv.experience}')

    # Add Skills
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 440, 'Skills')
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, 420, f'{cv.skills}')

    # Add Interests
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 390, 'Interests')
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, 370, f'{cv.interests}')

    # Add Achievements
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 340, 'Achievements')
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, 320, f'{cv.achievements}')

    # Add References
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 290, 'References')
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, 270, f'{cv.references}')

    pdf.showPage()
    pdf.save()

    return response

def generate_cv_pdf(request, cv_id):
    # Generate the PDF using the utility function
    pdf_response = generate_pdf(cv_id)
    
    return pdf_response


'''
def generate_cv_pdf(request, cv_id):
    try:
        cv = CV.objects.get(pk=cv_id)
    except CV.DoesNotExist:
        raise Http404("CV does not exist")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={cv.name}_cv.pdf'

    pdf = canvas.Canvas(response, pagesize=letter)

    # Add Title
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawString(50, 750, 'Curriculum Vitae')
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 730, '------------------')

    # Add Image (at top right corner)
    if cv.image:
        img = ImageReader(cv.image.path)
        pdf.drawImage(img, 550, 700, width=100, height=100, mask='auto')

    # Add Personal Information
    y_offset = 650  # Initial y-coordinate for personal information
    personal_info = [
        f'Name: {cv.name}',
        f'Email: {cv.email}',
        f'Phone: {cv.phone}',
        f'Address: {cv.address}'
    ]
    for info in personal_info:
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y_offset, info)
        y_offset -= 20

    # Add About
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 590, 'About')
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, 570, f'{cv.about}')

    # Add Education
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 540, 'Education')
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, 520, f'{cv.education}')

    # Add Experience
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 490, 'Experience')
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, 470, f'{cv.experience}')

    # Add Skills
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 440, 'Skills')
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, 420, f'{cv.skills}')

    # Add Interests
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 390, 'Interests')
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, 370, f'{cv.interests}')

    # Add Achievements
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 340, 'Achievements')
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, 320, f'{cv.achievements}')

    # Add References
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 290, 'References')
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, 270, f'{cv.references}')

    pdf.showPage()
    pdf.save()

    return response
    '''