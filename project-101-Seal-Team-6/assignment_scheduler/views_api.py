# API to interact with database

from .models import Assignment, Student, Course
from datetime import datetime
from .google_cal_api import *
import pytz

"""
add_student(student_name)
get_student_calendar(student_name)
add_course(course_data, itr)
add_all_courses()
get_list_students()
get_list_courses()
get_list_student_courses(student_name)
add_course_to_student(course_data, student_name)
remove_course_from_student(course_key, student_name)
get_list_assignments(student_name)
add_assignment(assignment_data, student_name)
get_assignment(assignment_key, student_name)
delete_assignment(assignment_key)
remove_all_courses()
remove_all_students()
blacklist_assignment()
remove_blacklist()
"""

def add_student(student_name):
	stud = Student.objects.filter(stud_name=student_name)
	if len(stud) == 0:
		new_stud = Student()
		new_stud.stud_name = student_name
		new_stud.stud_calendar = create_calendar()
		new_stud.save()
		stud = new_stud
	else:
		stud = stud[0]
	return stud

def get_student_calendar(student_name):
	stud = add_student(student_name)
	front = "https://calendar.google.com/calendar/embed?src="
	back = "&ctz=America%2FNew_York"
	return {'Student_Calendar': front+stud.stud_calendar+back}

def add_course(course_data, itr):
	new_course = Course()
	new_course.course_num   = course_data[0]
	new_course.course_mn	= course_data[1]
	new_course.course_num2	= course_data[2]
	new_course.course_sec	= course_data[3]
	new_course.course_title = course_data[4]
	new_course.course_key	= itr
	new_course.save()

#checks if courses are in the database
#if not it reads through Courses.csv and adds them to the database
def add_all_courses():
	Course_List = Course.objects.all()
	if len(Course_List) < 100:
		file = open('Courses.csv').readlines()
		file.pop(0)
		itr = 0
		for line in file:
			line = line.split(',')
			line = [elem.rstrip() for elem in line]
			#process when the title has commas
			if len(line) > 5:
				title = line[4][1:]
				new_line = []
				for i in range(len(line)):
					if i < 4:
						new_line.append(line[i])
					if i > 4:
						title +=',' + line[i]
				title = title[:-1]
				new_line.append(title)
				line = new_line
			add_course(line, itr)
			itr += 1

def get_list_students():
	Student_List = Student.objects.all()
	context = {
		'Student_List':Student_List,
	}
	return context

def get_list_courses():
	Course_List = Course.objects.all()
	context = {
		'Course_List':Course_List,
	}
	return context

def get_list_student_courses(student_name):
	stud = add_student(student_name)
	context = {
		'Course_List':stud.stud_course.all()
	}
	return context


# Returns false if the course doesn't exist
# Returns true otherwise
def add_course_to_student(course_data, student_name):
	#Get/create the appropriate student
	stud = add_student(student_name)
	course = Course.objects.filter(course_num=course_data[0])
	if len(course) == 0:
		return 'failed_to_find_course'
	else:
		course = course[0]
	stud.stud_course.add(course)
	
def remove_course_from_student(course_key, student_name):
	stud = Student.objects.filter(stud_name = student_name)[0]
	course = Course.objects.filter(course_key = course_key)[0]
	stud.stud_course.remove(course)

def get_list_assignments(student_name):
	stud = add_student(student_name)
	Assignment_List1 = []
	Assignment_List = []
	blacklist = [elem for elem in stud.stud_blacklist.all()]
	for c in stud.stud_course.all():
		Assignment_List1.extend(Assignment.objects.filter(assi_course=c).all())
	for assi in Assignment_List1:
		if assi not in blacklist:
			Assignment_List.append(assi)
	Assignment_List.sort(key=lambda a: a.assi_due_date)
	Assignment_Course_List = [(assi, assi.assi_course.all()[0]) for assi in Assignment_List]
	context = {
		'Assignment_List':Assignment_List,
		'Assignment_Course_List': Assignment_Course_List,
	}
	return context

def add_assignment(assignment_data, student_name):
	stud = add_student(student_name)
	course = stud.stud_course.filter(course_key=assignment_data[0])
	if len(course) > 0:
		course = course[0]
	else:
		return
	new_assign = Assignment()
	new_assign.assi_title		= assignment_data[1]
	due_date = assignment_data[2]
	due_time = assignment_data[3]
	due_date += ' ' + due_time + ' EST'
	datetime_object = datetime.strptime(due_date, '%Y-%m-%d %H:%M %Z')
	new_assign.assi_due_date = datetime_object
	new_assign.assi_description = assignment_data[4]
	new_assign.save()
	new_assign.assi_course.add(course)
	new_assign.assi_event_id = create_event(new_assign, stud)

def get_assignment(assignment_key, student_name):
	stud = add_student(student_name)
	context = {}
	Assignment_List = get_list_assignments(stud)
	
	for assignment in Assignment_List["Assignment_List"]:
		if int(assignment.pk) == int(assignment_key):
			context = {'Assignment' : assignment}
			
	context.update({'Assi_Course': context['Assignment'].assi_course.all()[0]})
	return context

def delete_assignment(assignment_key):
	assignment = Assignment.objects.filter(pk=assignment_key)
	if len(assignment) != 0:
		assignment[0].delete()

def remove_all_courses(): #~~tread with caution~~
	Course.objects.all().delete()

def refresh_calendar(student_name):
	stud = add_student(student_name)
	assi_list = get_list_assignments(student_name)['Assignment_List']
	event_list = get_event_list(stud)
	events_to_add = []
	events_to_remove = []

	#decide which assignments to add that are not in the calendar but ARE on the student's list
	for assi in assi_list:
		exists = False
		for event in event_list:
			if assi.assi_event_id == event['id']:
				exists = True
		if exists == False:
			events_to_add.append(assi)
	#decide which assignments to remove from the calendar that aren't in the student's list
	for event in event_list:
		exists = False
		for assi in assi_list:
			if assi.assi_event_id == event['id']:
				exists = True
		if exists == False:
			events_to_remove.append(event['id'])

	#actually add the events to the calendar
	for assi in events_to_add:
		create_event(assi, stud)

	for event_id in events_to_remove:
		delete_event(event_id, stud)

def remove_all_students():
	Student.objects.all().delete()

def blacklist_assignment(assignment_key,student_name):
	stud = add_student(student_name)
	assignment = Assignment.objects.filter(pk = assignment_key)[0]
	stud.stud_blacklist.add(assignment)

def remove_blacklist(assignment_key,student_name):
	stud = add_Student(student_name)
	assignment = Assignment.objects.filter(pk = assignment_key)[0]
	stud.stud_blacklist.remove(assignment)

