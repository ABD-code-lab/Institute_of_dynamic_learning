# Contents of views:
# 1- Import Statements
# 2- Main Page view
# 3- Authentication views
# 4- Admin views
        #   4a- Dashboard
        #   4b- CRUD Teachers
        #   4c- CRUD Students
        #   4d- Birthdays
        #   4e- CRUD Events
        #   4f- CRUD Student Cards
        #   4g- Settings
        #   4h- Read Results 
        #   4i- CRUD Fee
        #   4j- CRUD Teacher's Attendance
# 5- Teacher views
        #   5a- Dashboard
        #   5b- Birthdays
        #   5c- Read Events
        #   5d- CRUD Results
        #   5e- Read Fee
        #   5f- Settings
        #   5g- Help
        #   5h- CRUD Diary 
        #   5i- CRUD Student's Attendance
# 6- Student views
        #   6a- Dashboard
        #   6b- Birthdays
        #   6c- Read Events
        #   6e- Read Fee
        #   6d- Read Results
        #   6h- Read Diary 
        #   6h- CRUD Reviews
        #   6i- Read Student's Attendance

                                            # --------------------
                                            # Import Statements 
                                            # --------------------

from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Result, Teacher, StudentAttendance, StudentFee, Event, TeacherAttendance, TeacherReview, Diary
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import get_user_model
from datetime import date
from django.db.models import Sum, Count
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import CustomUser

                                            # --------------------
                                            # Main page view 
                                            # --------------------

def main_view (req):
    return render (req, 'main.html')

                                            # --------------------
                                            # Authentication views 
                                            # --------------------

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        if get_user_model().objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})

        user = get_user_model().objects.create_user(username=username, password=password, role=role)
        login(request, user)

        if role == 'admin':
            return redirect('admin_dashboard')
        elif role == 'teacher':
            return redirect('teacher_dashboard')
        elif role == 'student':
            return redirect('student_dashboard')

    return render(request, 'authentication/signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'teacher':
                return redirect('teacher_dashboard')
            elif user.role == 'student':
                return redirect('student_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'authentication/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# -----------------------------------------------Start Admin Views-------------------------------------------- #

                                            # ------------------------
                                            # Admin Dashboard Views
                                            # ------------------------

@login_required()
def admin_dashboard(request):
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_events = Event.objects.count()
    teachers = Teacher.objects.order_by('-id')[:3]
    students = Student.objects.order_by('-id')[:3]
    name = request.user.username
    role = request.user.role
    data = StudentFee.objects.aggregate(
        amount_paid =Sum('amount_paid'),
        total_fee=Sum('total_fee'),
    )
    pending_fee = data['amount_paid'] - data['total_fee']

    if request.user.role != 'admin':
        return HttpResponseForbidden("You are not allowed here.")
    return render(request, 'dashboards/admin_dashboard.html', {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_events': total_events,
        'recent_teachers': teachers,
        'recent_students': students,
        'name': name,
        'role': role,
        'pending_fee': pending_fee,
    })

                                            # ------------------------
                                            # Admin - Teacher Views
                                            # ------------------------

def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'dashboards/admin/teachers/list.html', {'teachers': teachers})

def teacher_detail(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    return render(request, 'dashboards/admin/teachers/detail.html', {'teacher': teacher})

def teacher_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        phone = request.POST['phone']
        Teacher.objects.create(name=name, email=email, subject=subject, phone=phone)
        return redirect('teacher_list')
    return render(request, 'dashboards/admin/teachers/create.html')

def teacher_update(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    if request.method == 'POST':
        teacher.name = request.POST['name']
        teacher.email = request.POST['email']
        teacher.subject = request.POST['subject']
        teacher.phone = request.POST['phone']
        teacher.save()
        return redirect('teacher_list')
    return render(request, 'dashboards/admin/teachers/update.html', {'teacher': teacher})

def teacher_delete(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    if request.method == 'POST':
        teacher.delete()
        return redirect('teacher_list')
    return render(request, 'dashboards/admin/teachers/delete.html', {'teacher': teacher})

                                            # ------------------------
                                            # Admin - Student Views
                                            # ------------------------

def student_list(request):
    query = request.GET.get('search')
    students = Student.objects.all()

    if query:
        students = students.filter(Q(name__icontains=query))

    total_students = students.count()  

    paginator = Paginator(students, 30)
    page = request.GET.get('page')
    students = paginator.get_page(page)

    return render(request, 'dashboards/admin/students/student_list.html', {
        'students': students,
        'total_students': total_students,
    })

def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'dashboards/admin/students/student_detail.html', {'student': student})

def student_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        roll_no = request.POST['roll_no']
        subject = request.POST['subject']
        date_of_birth = request.POST['date_of_birth']

        Student.objects.create(
            name=name,
            email=email,
            roll_no=roll_no,
            subject=subject,
            date_of_birth=date_of_birth
        )
        return redirect('student_list')

    return render(request, 'dashboards/admin/students/student_form.html')

def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        student.name = request.POST['name']
        student.email = request.POST['email']
        student.roll_no = request.POST['roll_no']
        student.subject = request.POST['subject']
        student.date_of_birth = request.POST['date_of_birth']
        student.save()
        return redirect('student_list')

    return render(request, 'dashboards/admin/students/student_form.html', {'student': student})

def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        student.delete()
        return redirect('student_list')

    return render(request, 'dashboards/admin/students/student_confirm_delete.html', {'student': student})

                                            # ------------------------
                                            # Admin - Birthday Views
                                            # ------------------------

def birthdays_today(request):
    today = date.today()
    students = Student.objects.filter(
        date_of_birth__month=today.month,
    )
    return render(request, 'dashboards/admin/birthday/birthdays.html', {
        'students': students
    })

                                            # ------------------------
                                            # Admin - Events Views
                                            # ------------------------

def event_list(request):
    query = request.GET.get('search')
    events = Event.objects.all().order_by('-start_date')
    if query:
        events = events.filter(Q(title__icontains=query) | Q(location__icontains=query))
    
    paginator = Paginator(events, 10)
    page = request.GET.get('page')
    events = paginator.get_page(page)
    
    return render(request, 'dashboards/admin/events/event_list.html', {'events': events})

def event_create(request):
    if request.method == 'POST':
        Event.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            location=request.POST['location'],
            start_date=request.POST['start_date'],
            end_date=request.POST['end_date']
        )
        return redirect('event_list')
    return render(request, 'dashboards/admin/events/event_form.html')

def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.title = request.POST['title']
        event.description = request.POST['description']
        event.location = request.POST['location']
        event.start_date = request.POST['start_date']
        event.end_date = request.POST['end_date']
        event.save()
        return redirect('event_list')
    return render(request, 'dashboards/admin/events/event_form.html', {'event': event})

def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'dashboards/admin/events/event_confirm_delete.html', {'event': event})

                                            # ------------------------
                                            # Admin - Cards Views
                                            # ------------------------

from django.shortcuts import render, get_object_or_404
from .models import Student

def cards_student_list(request):
    students = Student.objects.all()
    return render(request, 'dashboards/admin/cards/cards_student_list.html', {'students': students})

def print_card(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'dashboards/admin/cards/print_card.html', {'student': student})

                                            # ------------------------
                                            # Admin - Settings Views
                                            # ------------------------

@login_required
def settings_view(request):
    if request.method == 'POST':
        request.user.email = request.POST.get('email')
        new_password = request.POST.get('password')

        if new_password:
            request.user.set_password(new_password)
        
        request.user.save()
        return redirect('dashboard_settings')

    return render(request, 'dashboards/admin/setting/settings.html')

@login_required
def appearance_settings(request):
    context = {
        'user': request.user,
    }
    return render(request, 'dashboards/admin/settings/appearance.html', context)

                                            # ------------------------
                                            # Admin - Result View
                                            # ------------------------

def admin_result_view (req):
    results = Result.objects.select_related('student').all()
    total_students = Student.objects.count()
    top_result = Result.objects.order_by('-marks_obtained').first()
    top_result_percentage = (top_result.marks_obtained/top_result.total_marks)*100
    data = Result.objects.aggregate(
        total_obtained=Sum('marks_obtained'),
        total_full=Sum('total_marks'),
        total_results=Count('id')
    )
    average_percentage = (data['total_obtained'] / data['total_full']) * 100
    average_percentage = round(average_percentage, 2) 
    return render (req, 'dashboards/admin/result/result_list.html', {'results': results,
                                                                           'total_students': total_students,
                                                                           'top_result' : top_result,
                                                                           'top_result_percentage':top_result_percentage,
                                                                           'average_percentage':average_percentage,})

                                            # ------------------------
                                            # Admin - Fee Views
                                            # ------------------------

def add_fee(request):
    students = Student.objects.all()
    if request.method == 'POST':
        student_id = request.POST.get('student')
        student = Student.objects.get(id=student_id)
        amount_paid = request.POST.get('amount_paid')
        total_fee = request.POST.get('total_fee')
        is_paid = 'is_paid' in request.POST

        StudentFee.objects.create(
            student=student,
            amount_paid=amount_paid,
            total_fee=total_fee,
            is_paid=is_paid
        )
        return redirect('fee_list')
    return render(request, 'dashboards/admin/fees/fee_form.html', {'students': students})

def admin_fee_list(request):
    fees = StudentFee.objects.all()
    return render(request, 'dashboards/admin/fees/fee_list.html', {'fees': fees})

def delete_fee(request, pk):
    fee = get_object_or_404(StudentFee, pk=pk)
    if request.method == 'POST':
        fee.delete()
        return redirect('fee_list')
    return render(request, 'dashboards/admin/fees/fee_confirm_delete.html', {'fee': fee})

def update_fee(request, pk):
    fee = get_object_or_404(StudentFee, pk=pk)
    students = Student.objects.all()
    if request.method == 'POST':
        student_id = request.POST.get('student')
        student = Student.objects.get(id=student_id)
        fee.student = student
        fee.amount_paid = request.POST.get('amount_paid')
        fee.total_fee = request.POST.get('total_fee')
        fee.is_paid = 'is_paid' in request.POST
        fee.save()
        return redirect('fee_list')
    return render(request, 'dashboards/admin/fees/fee_form.html', {'fee': fee, 'students': students})

                                            # ---------------------------------
                                            # Admin - Teacher's Attendance View
                                            # ---------------------------------

def attendance_list(request):
    records = TeacherAttendance.objects.all().order_by('-date')
    return render(request, 'dashboards/admin/attendance/attendance_list.html', {'records': records})

def add_attendance(request):
    teachers = Teacher.objects.all()
    if request.method == 'POST':
        teacher_name = request.POST['teacher_name']
        date_value = request.POST['date']
        status = request.POST['status']
        TeacherAttendance.objects.create(
            teacher_name=teacher_name,
            date=date_value,
            status=status
        )
        return redirect('attendance_list')
    return render(request, 'dashboards/admin/attendance/add_attendance.html', {'teachers':teachers})

def edit_attendance(request, pk):
    record = get_object_or_404(TeacherAttendance, pk=pk)
    if request.method == 'POST':
        record.teacher_name = request.POST['teacher_name']
        record.date = request.POST['date']
        record.status = request.POST['status']
        record.save()
        return redirect('attendance_list')
    return render(request, 'dashboards/admin/attendance/edit_attendance.html', {'record': record})

def delete_attendance(request, pk):
    record = get_object_or_404(TeacherAttendance, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('attendance_list')
    return render(request, 'dashboards/admin/attendance/delete_attendance.html', {'record': record})

def teachers_attendance_list (req):
    records = TeacherAttendance.objects.all().order_by('-date')
    return render (req, 'dashboards/teacher/attendance/attendance_list.html', {'records' : records})



# -----------------------------------------------Ended Admin Views-------------------------------------------- #



# -----------------------------------------------Start Teacher Views------------------------------------------ #



                                            # ------------------------
                                            # Teacher Dashboard Views
                                            # ------------------------

@login_required
def teacher_dashboard(request):
    if request.user.role != 'teacher':
        return HttpResponseForbidden("You are not allowed here.")

    total_students = Student.objects.count()
    upcoming_events = Event.objects.count()
    today = date.today()
    students_birthdays = Student.objects.filter(date_of_birth__month=today.month)
    total_events = Event.objects.all().order_by('-start_date')
    name = request.user.username
    role = request.user.role

    data = Result.objects.aggregate(
        total_obtained=Sum('marks_obtained'),
        total_full=Sum('total_marks'),
        total_results=Count('id')
    )
    total_obtained = data['total_obtained'] or 0
    total_full = data['total_full'] or 0
    average_percentage = (total_obtained / total_full * 100) if total_full else 0
    average_percentage = round(average_percentage, 2)

    student_fee = StudentFee.objects.select_related('student').order_by('-id')[:3]

    fee_data = StudentFee.objects.aggregate(
        amount_paid=Sum('amount_paid'),
        total_amount=Sum('total_fee'),
        total_results=Count('id')
    )
    amount_paid = fee_data['amount_paid'] or 0
    total_amount = fee_data['total_amount'] or 0
    fee_average_percentage = (amount_paid / total_amount * 100) if total_amount else 0
    fee_average_percentage = round(fee_average_percentage, 2)  # Fixed: Use fee_average_percentage

    fee_data_again = StudentFee.objects.aggregate(
        amount_paid=Sum('amount_paid'),
        total_amount=Sum('total_fee'),
    )
    total_pending_fee = (fee_data_again['total_amount'] or 0) - (fee_data_again['amount_paid'] or 0)

    result = Result.objects.order_by('-id')[:4]

    diaries = Diary.objects.order_by('-id')[:3]

    students_attendance = StudentAttendance.objects.order_by('-id')[:4]

    context = {
        'total_students': total_students,
        'upcoming_events': upcoming_events,
        'students_birthdays': students_birthdays,
        'total_events': total_events,
        'name': name,
        'role': role,
        'average_percentage': average_percentage,
        'fee_average_percentage': fee_average_percentage,
        'total_pendng_fee': total_pending_fee,
        'student_fee': student_fee,
        'result': result,
        'diaries' : diaries,
        'students_attendance' : students_attendance,
    }

    return render(request, 'dashboards/teacher_dashboard.html', context)

                                            # ------------------------
                                            # Teacher - Birthday View
                                            # ------------------------

def teacher_birthdays_view (req):
    today = date.today()
    students_birthdays = Student.objects.filter(
        date_of_birth__month=today.month,
    )
    return render (req, 'dashboards/teacher/birthday/birthday.html', {
        'students' : students_birthdays,
    })

                                            # ------------------------
                                            # Teacher - Events View
                                            # ------------------------

def teacher_events_view (req):
    events = Event.objects.all().order_by('-start_date')
    return render (req, 'dashboards/teacher/events/events_list.html', {
        'events' : events,
    })

                                            # ------------------------
                                            # Teacher - Results Views
                                            # ------------------------

def result_list(request):
    results = Result.objects.select_related('student').all()
    total_students = Student.objects.count()
    top_result = Result.objects.order_by('-marks_obtained').first()
    top_result_percentage = (top_result.marks_obtained/top_result.total_marks)*100
    data = Result.objects.aggregate(
        total_obtained=Sum('marks_obtained'),
        total_full=Sum('total_marks'),
        total_results=Count('id')
    )
    average_percentage = (data['total_obtained'] / data['total_full']) * 100
    average_percentage = round(average_percentage, 2)  

    return render(request, 'dashboards/teacher/result/results_list.html', {'results': results,
                                                                           'total_students': total_students,
                                                                           'top_result' : top_result,
                                                                           'top_result_percentage':top_result_percentage,
                                                                           'average_percentage':average_percentage,})

def result_create(request):
    students = Student.objects.all()
    if request.method == 'POST':
        student_id = request.POST['student']
        exam_name = request.POST['exam_name']
        marks_obtained = request.POST['marks_obtained']
        total_marks = request.POST['total_marks']
        result_date = request.POST['result_date']

        student = get_object_or_404(Student, id=student_id)
        Result.objects.create(
            student=student,
            exam_name=exam_name,
            marks_obtained=marks_obtained,
            total_marks=total_marks,
            result_date=result_date
        )
        return redirect('result_list')

    return render(request, 'dashboards/teacher/result/result_form.html', {'students': students})

def result_update(request, id):
    result = get_object_or_404(Result, id=id)
    students = Student.objects.all()
    if request.method == 'POST':
        result.student = get_object_or_404(Student, id=request.POST['student'])
        result.exam_name = request.POST['exam_name']
        result.marks_obtained = request.POST['marks_obtained']
        result.total_marks = request.POST['total_marks']
        result.result_date = request.POST['result_date']
        result.save()
        return redirect('result_list')

    return render(request, 'dashboards/teacher/result/result_form.html', {'result': result, 'students': students})

def result_confirm_delete(request, id):
    result = get_object_or_404(Result, id=id)
    if request.method == 'POST':
        result.delete()
        return redirect('result_list')
    return render(request, 'dashboards/teacher/result/result_confirm_delete.html', {'result': result})

                                            # ------------------------
                                            # Teacher - Fee View
                                            # ------------------------

def teacher_fee_list(request):
    fees = StudentFee.objects.all()
    return render(request, 'dashboards/teacher/fees/fee_list.html', {'fees': fees})

                                            # ------------------------
                                            # Teacher - Settings View
                                            # ------------------------

@login_required
def teacher_settings_view(request):
    name = request.user.username
    role = request.user.role
    return render(request, 'dashboards/teacher/setting/settings.html', {
        'name' : name,
        'role' : role,
    })

                                            # ------------------------
                                            # Teacher - Help View
                                            # ------------------------

@login_required
def help_view (request):
    return render(request, 'dashboards/teacher/help/help.html')

                                            # ------------------------
                                            # Teacher - Diary Views
                                            # ------------------------

def diary_list(request):
    diaries = Diary.objects.all()
    return render(request, 'dashboards/teacher/diary/list.html', {'diaries': diaries})

def diary_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        date = request.POST['date']
        Diary.objects.create(title=title, content=content, date=date)
        return redirect('diary_list')
    return render(request, 'dashboards/teacher/diary/create.html')

def diary_update(request, pk):
    diary = get_object_or_404(Diary, pk=pk)
    if request.method == 'POST':
        diary.title = request.POST['title']
        diary.content = request.POST['content']
        diary.date = request.POST['date']
        diary.save()
        return redirect('diary_list')
    return render(request, 'dashboards/teacher/diary/update.html', {'diary': diary})

def diary_delete(request, pk):
    diary = get_object_or_404(Diary, pk=pk)
    if request.method == 'POST':
        diary.delete()
        return redirect('diary_list')
    return render(request, 'dashboards/teacher/diary/delete.html', {'diary': diary})

                                            # -----------------------------------
                                            # Teacher - Student's Attendance View
                                            # -----------------------------------

def students_attendance_list(request):
    records = StudentAttendance.objects.all().order_by('-date')
    return render(request, 'dashboards/teacher/student-attendance/attendance_list.html', {'records': records})

def students_add_attendance(request):
    students = Student.objects.all()
    if request.method == 'POST':
        student_name = request.POST['student_name']
        date = request.POST['date']
        status = request.POST['status']
        StudentAttendance.objects.create(
            student_name=student_name,
            date=date,
            status=status
        )
        return redirect('student_attendance_list')
    return render(request, 'dashboards/teacher/student-attendance/add_attendance.html', {
        'students' : students,
    })

def students_edit_attendance(request, pk):
    record = get_object_or_404(StudentAttendance, pk=pk)
    if request.method == 'POST':
        record.student_name = request.POST['student_name']
        record.date = request.POST['date']
        record.status = request.POST['status']
        record.save()
        return redirect('student_attendance_list')
    return render(request, 'dashboards/teacher/student-attendance/edit_attendance.html', {'record': record})

def students_delete_attendance(request, pk):
    record = get_object_or_404(StudentAttendance, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('student_attendance_list')
    return render(request, 'dashboards/teacher/student-attendance/delete_attendance.html', {'record': record})



# -----------------------------------------------Ended Teacher Views------------------------------------------ #



# -----------------------------------------------Start Student Views------------------------------------------ #



                                            # ------------------------
                                            # Student Dashboard Views
                                            # ------------------------

@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return HttpResponseForbidden("You are not allowed here.")
    
    name = request.user.username
    last_login = request.user.last_login
    role = request.user.role
    date_joined = request.user.date_joined
    id = request.user.id

    events_count = Event.objects.count()
    # Calculate average percentage for results
    data = Result.objects.aggregate(
        total_obtained=Sum('marks_obtained'),
        total_full=Sum('total_marks'),
        total_results=Count('id')
    )
    # Handle None or zero cases
    total_obtained = data['total_obtained'] or 0
    total_full = data['total_full'] or 0
    average_percentage = (total_obtained / total_full * 100) if total_full else 0
    average_percentage = round(average_percentage, 2)

    return render(request, 'dashboards/student_dashboard.html', {
        'name' : name,
        'role' : role,
        'last_login' : last_login, 
        'date_joined' : date_joined,
        'id' : id,
        'events_count' : events_count,
        'average_percentage' : average_percentage,
    })

                                            # ------------------------
                                            # Student - Birthday View
                                            # ------------------------

def student_birthdays_view(request):
    today = date.today()
    students = Student.objects.filter(
        date_of_birth__month=today.month,
    )
    return render(request, 'dashboards/student/birthday/birthday.html', {
        'students': students
    })

                                            # ------------------------
                                            # Student - Events View
                                            # ------------------------

def student_events_view (req):
    events = Event.objects.all().order_by('-start_date')
    return render (req, 'dashboards/student/events/events_list.html', {
        'events' : events,
    })


                                            # ------------------------
                                            # Student - Fee Views
                                            # ------------------------

def student_fee_list(request):
    fees = StudentFee.objects.all()
    return render(request, 'dashboards/student/fees/fee_list.html', {'fees': fees})



                                            # ------------------------
                                            # Student - Result View
                                            # ------------------------

def student_result_view (req):
    results = Result.objects.select_related('student').all()
    total_students = Student.objects.count()
    top_result = Result.objects.order_by('-marks_obtained').first()
    top_result_percentage = (top_result.marks_obtained/top_result.total_marks)*100
    data = Result.objects.aggregate(
        total_obtained=Sum('marks_obtained'),
        total_full=Sum('total_marks'),
        total_results=Count('id')
    )
    average_percentage = (data['total_obtained'] / data['total_full']) * 100
    average_percentage = round(average_percentage, 2) 
    return render (req, 'dashboards/student/result/result_list.html', {'results': results,
                                                                           'total_students': total_students,
                                                                           'top_result' : top_result,
                                                                           'top_result_percentage':top_result_percentage,
                                                                           'average_percentage':average_percentage,})



                                            # ------------------------
                                            # Student - Review Views
                                            # ------------------------

def review_list(request):
    reviews = TeacherReview.objects.all().order_by('-created_at')
    return render(request, 'dashboards/student/review/review_list.html', {'reviews': reviews})

def add_review(request):
    if request.method == 'POST':
        teacher_name = request.POST['teacher_name']
        rating = request.POST['rating']
        comment = request.POST['comment']
        TeacherReview.objects.create(
            teacher_name=teacher_name,
            rating=rating,
            comment=comment
        )
        return redirect('review_list')
    return render(request, 'dashboards/student/review/add_review.html')

def edit_review(request, pk):
    review = get_object_or_404(TeacherReview, pk=pk)
    if request.method == 'POST':
        review.teacher_name = request.POST['teacher_name']
        review.rating = request.POST['rating']
        review.comment = request.POST['comment']
        review.save()
        return redirect('review_list')
    return render(request, 'dashboards/student/review/edit_review.html', {'review': review})

def delete_review(request, pk):
    review = get_object_or_404(TeacherReview, pk=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('review_list')
    return render(request, 'dashboards/student/review/delete_review.html', {'review': review})



                                            # ------------------------
                                            # Student - Attendance View
                                            # ------------------------

def students_attendance_view (request):
    records = StudentAttendance.objects.all().order_by('-date')
    return render (request, 'dashboards/student/attendance/attendance_list.html', {
        'records' : records,
    })



# -----------------------------------------------Ended Student Views------------------------------------------ #