from django.urls import path
from . import views

app_name = 'equipment'
urlpatterns = [
    path('', views.index, name='index'),
    path('update', views.update, name='update')
]
