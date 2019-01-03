from django.contrib import admin

from .models import Student, Assignment, Course

admin.site.register(Student)
admin.site.register(Assignment)
admin.site.register(Course)