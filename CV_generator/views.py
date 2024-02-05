from django.shortcuts import render, redirect, HttpResponse, Http404
from .models import CV
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.units import inch
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
        return HttpResponse("CV does not exist")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{cv.name}_CV.pdf"'

    # Create PDF
    pdf_buffer = response
    doc = SimpleDocTemplate(pdf_buffer, rightMargin=0.5*inch, leftMargin=0.5*inch, topMargin=0.5*inch, bottomMargin=0.5*inch, pagesize=letter)

    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    body_style = styles["BodyText"]

    # Story to hold all the flowables
    story = []

    # Add Title
    title = Paragraph("Curriculum Vitae", title_style)
    story.append(title)
    story.append(Spacer(1, 12))

    # Add Image
    if cv.image:
        img_path = cv.image.path
        img = Image(img_path, width=1.5*inch, height=1.5*inch)
        img.hAlign = 'RIGHT'
        story.append(img)
        story.append(Spacer(1, 12))

    # Add Personal Information
    personal_info = [
        f'<b>Name:</b> {cv.name}',
        f'<b>Email:</b> {cv.email}',
        f'<b>Phone:</b> {cv.phone}',
        f'<b>Address:</b> {cv.address}'
    ]
    for info in personal_info:
        p = Paragraph(info, body_style)
        story.append(p)

    # Add About
    story.append(Spacer(1, 12))
    story.append(Paragraph("About", heading_style))
    story.append(Paragraph(cv.about, body_style))

    # Add Education
    story.append(Spacer(1, 12))
    story.append(Paragraph("Education", heading_style))
    story.append(Paragraph(cv.education, body_style))

    # Add Experience
    story.append(Spacer(1, 12))
    story.append(Paragraph("Experience", heading_style))
    story.append(Paragraph(cv.experience, body_style))

    # Add Skills
    story.append(Spacer(1, 12))
    story.append(Paragraph("Skills", heading_style))
    story.append(Paragraph(cv.skills, body_style))

    # Add Interests
    story.append(Spacer(1, 12))
    story.append(Paragraph("Interests", heading_style))
    story.append(Paragraph(cv.interests, body_style))

    # Add Achievements
    story.append(Spacer(1, 12))
    story.append(Paragraph("Achievements", heading_style))
    story.append(Paragraph(cv.achievements, body_style))

    # Add References
    story.append(Spacer(1, 12))
    story.append(Paragraph("References", heading_style))
    story.append(Paragraph(cv.references, body_style))

    # Build the PDF
    doc.build(story)

    return response

def generate_cv_pdf(request, cv_id):
    # Generate the PDF using the utility function
    pdf_response = generate_pdf(cv_id)
    
    return pdf_response