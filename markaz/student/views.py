from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from principle.views import *
from teacher.models import *
from principle.models import *
from itertools import groupby
from django.http import HttpResponse, JsonResponse, FileResponse, HttpResponseForbidden
from xhtml2pdf import pisa
from weasyprint import HTML as WeasyHTML
from weasyprint import HTML
from django.template.loader import get_template
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from django.utils import timezone
from django.views.decorators.http import require_http_methods, require_POST
from datetime import timedelta
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login, logout
from student.mixins import student_required,StudentRequiredMixin
# Create your views here.


def no_permission(request):
    return render(request, 'student/no_permission.html')

# Student Home

class StudentHome(StudentRequiredMixin,View):
    def get(self, request):
        return render(request, 'student/studenthome.html')


# View Notification

class SeeNotificationView(StudentRequiredMixin,View):

    def get(self, request):
        student = request.user.student
        current_time = timezone.now()

        scheduled_notifications = Notification.objects.filter(
            recipient=student,
            scheduled_at__lte=current_time,
            seen=False
        ).order_by('-scheduled_at').first()
        
        if scheduled_notifications:
            scheduled_notifications.seen = True
            scheduled_notifications.save()
            sender_name = scheduled_notifications.sender.name
            notification_message = f"{sender_name}: {scheduled_notifications.message}"
        else:
            notification_message = None
        
        return JsonResponse({'notification_message': notification_message})

# View Study Material

class MaterialsList(View):
    def get(self, request):
        study_materials = StudyMaterial.objects.all()
        context = {
            'study_materials' : study_materials,
        }
        return render(request, 'student/materials_list.html', context)

class ViewMaterials(StudentRequiredMixin,View):

    def get(self, request, material_id):
        material = get_object_or_404(StudyMaterial, pk=material_id)
        response = FileResponse(material.file)
        return response

# View Academic Details

class StudentAcademicDetailView(StudentRequiredMixin,View):
    template_name = 'student/student_academic_detail.html'

    def get(self, request):
        student = request.user.student
        academic_details = AcademicDetail.objects.filter(student=student)

        grouped_academic_details = self.group_academic_details(academic_details)

        context = {
            'student': student,
            'academic_details': academic_details,
            'grouped_academic_details': grouped_academic_details,
        }

        return render(request, self.template_name, context)

    def group_academic_details(self, academic_details):
        grouped_academic_details = {}
        current_exam = None
        current_course = None
        details_list = []

        for detail in academic_details:
            if current_exam != detail.exam or current_course != detail.course:
                if current_exam is not None and current_course is not None:
                    grouped_academic_details[(current_exam, current_course)] = {
                        'rowspan': len(details_list),
                        'details': details_list,
                        'total_score': sum(detail.individual_score for detail in details_list),
                        'overall_grade': self.calculate_overall_grade(details_list),
                    }
                current_exam = detail.exam
                current_course = detail.course
                details_list = []

            details_list.append(detail)

        if current_exam is not None and current_course is not None:
            grouped_academic_details[(current_exam, current_course)] = {
                'rowspan': len(details_list),
                'details': details_list,
                'total_score': sum(detail.individual_score for detail in details_list),
                'overall_grade': self.calculate_overall_grade(details_list),
            }

        return grouped_academic_details

    def calculate_overall_grade(self, details_list):
        total_score = sum(detail.individual_score for detail in details_list)

        if total_score >= 520:
            return 'A'
        elif total_score >= 400:
            return 'B'
        elif total_score >= 320:
            return 'C'
        elif total_score >= 240:
            return 'D'
        else:
            return 'F'

class StudentAcademicDetailPdfView(StudentRequiredMixin,View):
    
    def get(self, request):
        student = request.user.student
        academic_details = AcademicDetail.objects.filter(student=student)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="academic_details.pdf"'

        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []

        data = []
        data.append(['Exam', 'Course', 'Subject', 'Individual_Score', 'Grade'])

        displayed_exam = set()
        displayed_courses = set()

        current_exam = None
        details_list = []
        total_score = 0
        overall_grade = ''

        for detail in academic_details:
            if detail.exam not in displayed_exam or detail.course not in displayed_courses:
                if current_exam is not None:
                    data.append(['Total Score', '', '', total_score, ''])
                    overall_grade = self.calculate_overall_grade(details_list)
                    data.append(['overall grade', '', '', '', overall_grade])
                    total_score = 0
                    details_list = []

                data.append([detail.exam, detail.course, detail.subject, detail.individual_score, detail.grade])
                displayed_exam.add(detail.exam)
                displayed_courses.add(detail.course)

                current_exam = detail.exam
                total_score += detail.individual_score
                details_list.append(detail)
            else:
                data.append(['', '', detail.subject, detail.individual_score, detail.grade])
                total_score += detail.individual_score
                details_list.append(detail)

        if current_exam is not None:
            data.append(['Total Score', '', '', total_score, ''])
            overall_grade = self.calculate_overall_grade(details_list)
            data.append(['overall grade', '', '', '', overall_grade])

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(table)
        doc.build(elements)

        return response

    def calculate_overall_grade(self, details_list):
        total_score = sum(detail.individual_score for detail in details_list)

        if total_score >= 520:
            return 'A'
        elif total_score >= 400:
            return 'B'
        elif total_score >= 320:
            return 'C'
        elif total_score >= 240:
            return 'D'
        else:
            return 'F'

# For Downloading Course Completion Certificate in PDF Formate

class DownloadCertificateView(StudentRequiredMixin,View):

    def get(self, request, certificate_id):
        certificate = get_object_or_404(Certificate, id=certificate_id)
        template_path = 'student/certificate_template.html'
        context = {'certificate': certificate}
        template = get_template(template_path)
        html = template.render(context)

        pdf = self.generate_pdf_weasyprint(html)

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{certificate.student.name}_certificate.pdf"'

        return response

    def generate_pdf_weasyprint(self, html):
        weasy_html = WeasyHTML(string=html)
        pdf = weasy_html.write_pdf()
        return pdf

class CertificateListView(StudentRequiredMixin,View):

    def get(self, request):
        certificates = Certificate.objects.filter(student=request.user.student)
        return render(request, 'student/certificate.html', {'certificates': certificates})

# View Announcements

class StudentAnnouncements(StudentRequiredMixin,ListView):
    model = Announcement
    template_name = 'student/student_announcements.html'
    context_object_name = 'announcements'

    def get_queryset(self):
        one_day = timezone.now() - timedelta(days=1)
        queryset = Announcement.objects.filter(created_at__gte=one_day, show_to_students=True)
        return queryset



# view Rooms

class StudentRooms(StudentRequiredMixin,View):

    def get(self, request):
        rooms = Room.objects.all()
        context = {
            'rooms' : rooms,
        }
        return render(request, 'student/rooms.html', context)

    def get_queryset(self):
        user = self.request.user
        student = Student.objects.get(user=user)
        student_course = student.course
        queryset = Room.objects.filter(course=student_course)
        return queryset


class RoomView(StudentRequiredMixin,DetailView):

    model = Room
    template_name = 'student/room.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = self.object
        messages = Message.objects.filter(room=room)
        context['messages'] = messages
        return context



# view video library

class VideoLibrary(StudentRequiredMixin,View):

    def get(self, request):
        video_materials = self.get_queryset()
        context = {
            'video_materials': video_materials,
        }
        return render(request, 'student/video_material.html', context)

    def get_queryset(self):
        queryset = StudyMaterial.objects.filter(file__icontains='.mp4')
        return queryset


class StudentProfile(StudentRequiredMixin,DetailView):
    def get(self, request):
        student = request.user.student
        return render(request, 'student/student_profile.html', {'student': student})
