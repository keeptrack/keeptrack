from django.urls import path
from . import views

app_name = 'keeptrack_hire'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('<int:pk>/', views.HireView.as_view(), name='edit_hire'),

    path('<int:pk>/approve', views.approve_hire, name='approve_hire'),
    path('<int:pk>/reject/', views.reject_hire, name='reject_hire'),
    path('<int:pk>/unmark/', views.unmark_hire, name='unmark_hire'),

    path('<int:pk>/delete/', views.delete_hire, name='delete_hire'),
]
