from django.urls import path
from . import views

app_name = 'keeptrack_hire'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.HireView.as_view(), name='edit_hire'),
    path('<int:pk>/delete/', views.delete_hire, name='delete_hire'),
]
