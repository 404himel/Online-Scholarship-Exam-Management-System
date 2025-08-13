from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.utils.timezone import now
from .models import AdmitCardDownload

User = get_user_model()

def admit1(request):
    student = request.user
    return render(request, 'admit.html')

def download_admit(request):
    student = None
    if request.method == "POST":
        reg_no = request.POST.get("reg_no")

       
        try:
            student = User.objects.get(id=reg_no)  
        except User.DoesNotExist:
            return render(request, "download.html", {"error": "Student not found."})

    return render(request, "download.html", {"student": student})

def download_admit_list(request):
    student = None
    downloaded_users = AdmitCardDownload.objects.all()

    if request.method == "POST":
        reg_no = request.POST.get("reg_no")

        try:
            student = User.objects.get(id=reg_no)
        except User.DoesNotExist:
            return render(request, "admit.html", {"error": "Student not found.", "downloaded_users": downloaded_users})

    
    return render(request, "admit.html", {"student": student, "downloaded_users": downloaded_users})



def generate_pdf(request, reg_no):
    student = get_object_or_404(User, id=reg_no)
    
    # Log the download
    AdmitCardDownload.objects.create(user=student, download_time=now())
    
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="admit_card_{reg_no}.pdf"'
    
    # Create PDF
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    
    # Organization Name
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, height - 50, "Kazi Mofizul Islam Welfare Trust")
    
    # Organization Tagline - Use Helvetica instead of Helvetica-Italic
    p.setFont("Helvetica", 12)  # Changed from Helvetica-Italic to Helvetica
    p.drawCentredString(width / 2, height - 70, "For the good of humanity")
    
    # Admit Card Title
    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(width / 2, height - 100, "ADMIT CARD")
    
    # Divider line
    p.line(50, height - 110, width - 50, height - 110)
    
    # Student information
    p.setFont("Helvetica-Bold", 12)
    y_position = height - 140
    
    # Student basic info
    fields = [
        ("Student ID:", str(student.id) if student.id else "N/A"),
        ("Name:", f"{student.first_name or ''} {student.last_name or ''}"),
        ("School:", getattr(student, "school", "N/A")),
        ("Room No.:", "B-204"),  # Fixed value
        ("Seat No.:", "S-42")    # Fixed value
    ]
    
    for field, value in fields:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y_position, field)
        p.setFont("Helvetica", 12)
        p.drawString(150, y_position, value)
        y_position -= 20
    
    # Exam Rules
    y_position -= 20
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y_position, "Examination Rules:")
    y_position -= 20
    
    rules = [
        "Candidates must bring this admit card to every examination.",
        "Arrive at the examination center at least 30 minutes before scheduled time.",
        "Mobile phones and electronic devices are strictly prohibited.",
        "No candidate will be allowed entry after 15 minutes of exam commencement.",
        "No candidate is permitted to leave within the first hour of examination.",
        "Any form of malpractice will result in disqualification."
    ]
    
    p.setFont("Helvetica", 10)
    for rule in rules:
        p.drawString(60, y_position, "• " + rule)
        y_position -= 15
    
    # Signature lines
    y_position -= 30
    p.line(100, y_position, 200, y_position)
    p.setFont("Helvetica", 10)
    p.drawCentredString(150, y_position - 15, "Candidate's Signature")
    
    p.line(width - 200, y_position, width - 100, y_position)
    p.drawCentredString(width - 150, y_position - 15, "Controller of Examinations")
    
    p.showPage()
    p.save()
    return response