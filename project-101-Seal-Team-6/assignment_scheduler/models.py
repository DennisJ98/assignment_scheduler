from django.db import models
from django.utils import timezone
from django import forms
import datetime
from django.utils.timezone import now

class Course(models.Model):
	course_num	 = models.CharField(max_length=10, default='')
	course_mn	 = models.CharField(max_length=10, default='')
	course_num2  = models.CharField(max_length=10, default='')
	course_sec	 = models.CharField(max_length=10, default='')
	course_title = models.CharField(max_length=100, default='')
	course_key	 = models.CharField(max_length=10, default='')
	def __str__(self):
		return self.course_title

class Assignment(models.Model):
	assi_title = models.CharField(max_length=100)
	assi_due_date = models.DateTimeField('Due Date')
	assi_course = models.ManyToManyField(Course)
	assi_description = models.CharField(max_length=500, default='')
	assi_event_id = models.CharField(max_length=200, default='')
	def __str__ (self):
		return self.assi_title #don't name things with "name" - it breaks

class Student(models.Model):
	stud_name = models.CharField(max_length=30)
	stud_course = models.ManyToManyField(Course)
	stud_blacklist = models.ManyToManyField(Assignment)
	stud_calendar = models.CharField(max_length=200, default='')
	def __str__ (self):
		return self.stud_name