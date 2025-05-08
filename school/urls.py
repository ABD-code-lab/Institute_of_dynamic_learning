from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    # Main page
    path('', views.main_view, name='main'),
    # Authentication
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    # Dashboards
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),

                                    # ---------------------
                                    # Admin URLs
                                    # ---------------------

    # Admin - CRUD teachers
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/<int:id>/', views.teacher_detail, name='teacher_detail'),
    path('teachers/create/', views.teacher_create, name='teacher_create'),
    path('teachers/<int:id>/update/', views.teacher_update, name='teacher_update'),
    path('teachers/<int:id>/delete/', views.teacher_delete, name='teacher_delete'),
    # Admin - CRUD students
    path('students/', views.student_list, name='student_list'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/edit/', views.student_update, name='student_update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),
    # Admin - Birthdays
    path('birthdays/', views.birthdays_today, name='birthdays_today'),
    # Admin - CRUD Events
    path('events/', views.event_list, name='event_list'),
    path('events/create/', views.event_create, name='event_create'),
    path('event/update/<int:pk>/', views.event_update, name='event_update'),
    path('event/delete/<int:pk>/', views.event_delete, name='event_delete'),
    # Admin - Cards
    path('cards-student-list/', views.cards_student_list, name='cards_student_list'),
    path('print-card/<int:pk>/', views.print_card, name='print_card'),
    # Admin - Settings
    path('settings/', views.settings_view, name='dashboard_settings'),
    path('settings-appearance/', views.appearance_settings, name='appearance_settings'),
    # Admin - CRUD Fee Details
    path('admin-fee/', views.admin_fee_list, name='fee_list'),
    path('fee-add/', views.add_fee, name='add_fee'),
    path('fee-update/<int:pk>/', views.update_fee, name='fee-update'),
    path('fee-delete/<int:pk>/', views.delete_fee, name='fee-delete'),
    # Admin - Results
    path('admin-results/', views.admin_result_view, name='admin-results'),
    # Admin - CRUD Teaher's Attendance
    path('attendance-list/', views.attendance_list, name='attendance_list'),
    path('add-attendance/', views.add_attendance, name='add_attendance'),
    path('edit-attendance/<int:pk>/', views.edit_attendance, name='edit_attendance'),
    path('delete-attendance/<int:pk>/', views.delete_attendance, name='delete_attendance'),

                                    # ---------------------
                                    # Teacher URLs
                                    # ---------------------

    # Teacher - Birthdays
    path('teacher-birthdays/', views.teacher_birthdays_view, name='teacher-birthdays'),
    # Teacher - Events
    path('teacher-events/', views.teacher_events_view, name='teacher-events'),
    # Teacher - CRUD Results
    path('results/', views.result_list, name='result_list'),
    path('results/create/', views.result_create, name='result_create'),
    path('results/<int:id>/update/', views.result_update, name='result_update'),
    path('results/<int:id>/delete/', views.result_confirm_delete, name='result_delete'),
    # Teacher - Fee Details
    path('teacher-fee/', views.teacher_fee_list, name='fee_list'),
    # Teacher - Settings
    path('teacher-dashboard-settings/', views.teacher_settings_view, name='teacher-dashboard-settings'),
    # Teacher - Help
    path('help/', views.help_view, name='help'),
    # Teacher - CRUD Diary
    path('teacher-diary/', views.diary_list, name='diary_list'),
    path('diary-create/', views.diary_create, name='diary_create'),
    path('diary-update/<int:pk>/', views.diary_update, name='diary_update'),
    path('diary-delete/<int:pk>/', views.diary_delete, name='diary_delete'),
    # Teacher - Read Attendance
    path('teachers-attendance-list/', views.teachers_attendance_list, name='teachers-attendance-list'),
    # Teacher - CRUD Student's Attendance
    path('students-attendance-list/', views.students_attendance_list, name='student_attendance_list'),
    path('add-students-attendance/', views.students_add_attendance, name='add_student_attendance'),
    path('edit-students-attendance/<int:pk>/', views.students_edit_attendance, name='edit_student_attendance'),
    path('delete-students-attendance/<int:pk>/', views.students_delete_attendance, name='delete_student_attendance'),

                                    # ---------------------
                                    # Student URLs
                                    # ---------------------

    # Student - Birthdays
    path('student-birthdays/', views.student_birthdays_view, name='student-birthdays'),
    # Student - Events
    path('student-events/', views.student_events_view, name='student-events'),
    # Student - Results
    path('student-results/', views.student_result_view, name='student-results'),
    # Student - Fee
    path('student-fee/', views.student_fee_list, name='student-fee'),
    # Student - Birthdays
    # Student - CRUD Reviews
    path('teacher-reviews/', views.review_list, name='review_list'),
    path('add/', views.add_review, name='add_review'),
    path('edit/<int:pk>/', views.edit_review, name='edit_review'),
    path('delete/<int:pk>/', views.delete_review, name='delete_review'),
    # Student - Read Attendance
    path('attendance-list-students/', views.students_attendance_view, name='attendance-list-students'),
]
