# from django.urls import path
#
# from . import views
#
# urlpatterns = [
#     path('', views.index, name='index'),
# ]
from django.urls import path
from django.conf.urls import url
from django.urls import path, include 
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
	path('', views.SignUp.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    url('home/', views.home, name='home'),
	url(r'^get_new_course$', views.get_new_course, name='get_new_course'),
	url(r'^get_new_assignment$', views.get_new_assignment, name = 'get_new_assignment'),
	url(r'^remove_course$', views.remove_course, name = 'remove_course'),
	url(r'^get_assignment_details$', views.get_assignment_details, name = 'get_assignment_details'),
	url(r'^remove_assignment$', views.remove_assignment, name = 'remove_assignment'),
	url(r'^hide_assignment$', views.hide_assignment, name = 'hide_assignment'),
	#url(r'^get_new_credentials$', views.get_new_credentials, name ='get_new_credentials')
    ]
