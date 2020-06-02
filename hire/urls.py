from django.urls import path
from . import views

app_name = 'hire'
urlpatterns = [path('details', views.details, name='details'),
               path('', views.index, name='index')]
