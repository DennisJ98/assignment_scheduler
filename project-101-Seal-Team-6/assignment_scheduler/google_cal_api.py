import httplib2
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import pytz
from datetime import timedelta, datetime

service_account_email = 'service-account@uva-assignment-scheduler.iam.gserviceaccount.com'

CLIENT_SECRET_FILE = 'assignment_scheduler/client_secrets.json'

SCOPES = 'https://www.googleapis.com/auth/calendar'
scopes = [SCOPES]

class Service:
	service = None
	def get_service():
		if Service.service is None:
			credentials = ServiceAccountCredentials.from_json_keyfile_name(filename=CLIENT_SECRET_FILE,scopes=SCOPES)
			http = credentials.authorize(httplib2.Http())
			Service.service = build('calendar', 'v3', http=http)
			return Service.service
		else:
			return Service.service


def create_event(assignment, student):
	service = Service.get_service()
	start_datetime = assignment.assi_due_date
	event = service.events().insert(calendarId=student.stud_calendar, body={
		'summary': assignment.assi_title,
		'description': assignment.assi_description,
		'start': {'dateTime': start_datetime.isoformat(), 'timeZone' : 'America/New_York'},
		'end': {'dateTime': start_datetime.isoformat(), 'timeZone' : 'America/New_York'},
	}).execute()
	return event['id']
    
def create_calendar():
	service = Service.get_service()
	calendar = {
		'summary': 'Assignment Scheduler',
		'timeZone': 'America/New_York'
	}
	rule = {
		'scope': {
			'type': 'default'
			},
		'role' : 'reader'
	}
	created_calendar = service.calendars().insert(body=calendar).execute()
	created_rule = service.acl().insert(calendarId=created_calendar['id'], body=rule).execute()
	return created_calendar['id']
	
def get_event_list(Student):
	service = Service.get_service()
	events = service.events().list(calendarId=Student.stud_calendar).execute()
	return events['items']
	
def delete_event(event_id, student):
	service = Service.get_service()
	service.events().delete(calendarId=student.stud_calendar, eventId=event_id).execute()
