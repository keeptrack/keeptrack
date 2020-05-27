from django.urls import path
from . import views

urlpatterns = [path('details', views.details, name='details'),
               path('', views.index, name='index')]
