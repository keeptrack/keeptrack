from django.conf.urls import url
from . import views

app_name = 'cal'
urlpatterns = [
    url(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),
    url(r'^event/new/$', views.event, name='event_new'),
    url(r'^hire/new/$', views.hire, name='hire_new'),
    url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit')
]
