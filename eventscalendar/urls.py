from django.urls import path
from . import views

app_name = 'eventscalendar'
urlpatterns = [
    path('calendar', views.CalendarView.as_view(), name='calendar')
]
