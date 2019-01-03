from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .views_api import *
from .google_cal_api import *
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from .models import Assignment, Student, Course

"""
home(request, context=None)
get_new_course(request)
remove_course(request)
remove_assignment(request)
SignUp(generic.CreateView)
get_new_assignment(request)
get_assignment_details(request)
"""

def home(request, context=None):
	add_all_courses()
	if not context:
		context = {}
	if request.user:
		context.update(get_list_student_courses(request.user.username))
		context.update(get_list_assignments(request.user.username))
		context.update(get_student_calendar(request.user.username))
		refresh_calendar(request.user.username)
	template = loader.get_template('assignment_scheduler/home.html')
	return HttpResponse(template.render(context, request))


def get_new_course(request):
	context = {}
	if request.method == 'POST' and request.user:
		course_num   = request.POST.get('course_number', None)
		course_data = [course_num]
		error_code_course = add_course_to_student(course_data, request.user.username) #call to views api
		if error_code_course is not None:
			context = {'error_code_course':error_code_course}
	return home(request, context)

def remove_course(request):
	if request.method == 'POST' and request.user:
		course_key   = request.POST.get('course_key', None)
		if course_key != None:
			remove_course_from_student(course_key, request.user.username)
	return home(request)
		
def remove_assignment(request):
	if request.method == 'POST' and request.user:
		assignment_key = request.POST.get('remove_assignment_button', None)
		delete_assignment(assignment_key)
	return home(request)
	
def hide_assignment(request):
	if request.method == 'POST' and request.user:
		assignment_key = request.POST.get('hide_assignment_button', None)
		blacklist_assignment(assignment_key, request.user.username)
	return home(request)

class SignUp(generic.CreateView):
	form_class = UserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'assignment_scheduler/signup.html'
    
def get_new_assignment(request):
	if request.method == 'POST' and request.user:
		assignment_name_field        = request.POST.get('assignment_name_field', None)
		due_date_field               = request.POST.get('due_date_field', None)
		due_time_field               = request.POST.get('due_time_field', None)
		assignment_course_key        = request.POST.get('course_key', None)
		assignment_description_field = request.POST.get('assignment_description_field', None)
		if assignment_name_field == "" or due_date_field == "" or due_time_field == "" or assignment_course_key == None:
			return home(request)
		assignment_data = [assignment_course_key, assignment_name_field, due_date_field, due_time_field, assignment_description_field]
		add_assignment(assignment_data, request.user.username)
	return home(request)
	
def get_assignment_details(request):
	context = {}
	if request.method == 'POST' and request.user:
		assignment_key        = request.POST.get('assignment_key', None)
		context = get_assignment(assignment_key, request.user.username)
	return home(request, context)
		
