from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Authentication model

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"
    
# Teacher model

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    subject = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    joined_date = models.DateField(auto_now_add=True)
    date_of_birth = models.DateField(null=True, blank=True)  

    def __str__(self):
        return self.name
    
# Student model

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    roll_no = models.CharField(max_length=20, unique=True)
    subject = models.CharField(max_length=50)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.name
    
# Event model

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.title
    
# Result model

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=100)
    marks_obtained = models.IntegerField()
    total_marks = models.IntegerField()
    result_date = models.DateField()

    def __str__(self):
        return f"{self.student.name} - {self.exam_name}"
    
# Fee model

class StudentFee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    total_fee = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.name} - {'Paid' if self.is_paid else 'Unpaid'}"

# Diary model

class Diary(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.title

# Teacher review model

class TeacherReview(models.Model):
    teacher_name = models.CharField(max_length=100)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.teacher_name} - {self.rating} Stars"

# Teacher attendance model

class TeacherAttendance(models.Model):
    teacher_name = models.CharField(max_length=100)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f"{self.teacher_name} - {self.date} - {self.status}"

# Student attendance model

class StudentAttendance(models.Model):
    student_name = models.CharField(max_length=100)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f"{self.student_name} - {self.date} - {self.status}"