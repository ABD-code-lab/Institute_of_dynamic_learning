from django.contrib import admin
from .models import *

admin.site.register(CustomUser)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Event)
admin.site.register(Result)
admin.site.register(StudentFee) 