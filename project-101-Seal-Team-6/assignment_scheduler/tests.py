from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from .views_api import *
from datetime import datetime
from django.utils import timezone
from django.utils.timezone import now
# Create your tests here.
# Adding course that doesn't exist

class use_home_Template1(TestCase):
	#this tests adding an assignment without a course
	#for some reason, tests aren't run with funciton name "add_assignment_no_course"
	#also test returns an error if class name is "test_add_assignment_no_course"
	def test_redirect_home1(self):
		name='TEST_Student'
		add_student(name)
		student=Student.objects.all()[0]
		course_data = []
		time = timezone.now()
		assignment_data = ['Test Assignment', time, course_data, 'This is a test description','1']
		add_assignment(assignment_data, name)
		self.assertEquals(len(Assignment.objects.all()),0)
		remove_all_courses()
		remove_all_students()


class use_home_Template(TestCase):

	def test_redirect_home(self):
		response = self.client.get('/home/')
		self.assertTemplateUsed(response,'assignment_scheduler/home.html')
		self.assertTemplateNotUsed(response, 'assignment_scheduler/signup.html')

class use_signup_Template(TestCase):

	def test_redirect_signup(self):
		response = self.client.get('')
		self.assertTemplateUsed(response,'assignment_scheduler/signup.html')
		self.assertTemplateNotUsed(response, 'assignment_scheduler/home.html')

class test_Login(TestCase):

	def test_user_log_in(self):
		response = self.client.get('')
		user = User.objects.create(username='testuser')
		user.set_password('12345')
		user.save()

		c = Client()
		logged_in = c.login(username='testuser', password='12345')
		self.assertTrue(logged_in)
		

class test_Courses(TestCase):

	def test_add_course(self):
		response = self.client.get('')
		# create test user
		user = User.objects.create(username='testuser')
		user.set_password('12345')
		user.save()
		
		#sign up for Advanced Software
		add_course_to_student(['16489'], user)
		courses = get_list_student_courses(user)
		for c in courses["Course_List"]:
			self.assertTrue(c.course_num == '16489')
			
	def test_remove_course(self):
		response = self.client.get('')
		# create test user
		user = User.objects.create(username='testuser')
		user.set_password('12345')
		user.save()
		
		#sign up for Advanced Software
		add_course_to_student(['16489'], user)
		courses = get_list_student_courses(user)
		
		#remove course from student and check if list of courses length is 0
		for c in courses["Course_List"]:
			remove_course_from_student(c.course_key, user)
			
		self.assertTrue(len(courses["Course_List"]) == 0)
		
class test_Assignment(TestCase):
	
	def test_add_assignment(self):
		response = self.client.get('')
		# create test user
		user = User.objects.create(username='testuser')
		user.set_password('12345')
		user.save()
		
		#sign up for Advanced Software, add assignment
		add_course_to_student(['16489'], user)
		courses = get_list_student_courses(user)
		
		for c in courses["Course_List"]:
			assi = [c.course_key, "Title", "2018-12-01", "12:00", "desc"]
			add_assignment(assi, user)
			assi_list = get_list_assignments(user)
			self.assertTrue(len(assi_list["Assignment_List"]) == 1)
		