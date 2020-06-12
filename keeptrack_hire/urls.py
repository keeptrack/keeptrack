from django.urls import path
from . import views

app_name = 'keeptrack_hire'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('<int:pk>/', views.HireView.as_view(), name='edit_hire'),
    path('<int:pk>/discount/', views.give_discount, name='set_discount'),

    path('<int:pk>/approve', views.approve_hire, name='approve_hire'),
    path('<int:pk>/reject/', views.reject_hire, name='reject_hire'),
    path('<int:pk>/unmark/', views.unmark_hire, name='unmark_hire'),

    path('<int:pk>/assets/', views.UpdateAssetsView.as_view(), name='update_assets'),
    path('<int:pk>/assets/<int:asset>/remove/', views.remove_asset, name='remove_asset'),

    path('<int:pk>/customitems/', views.UpdateCustomView.as_view(), name='update_custom'),
    path('<int:pk>/customitems/<int:item>/remove/', views.remove_custom, name='remove_custom'),

    path('<int:pk>/assets/avail.json', views.AvailableAssetsJsonView.as_view(), name='available_assets'),

    path('<int:pk>/delete/', views.delete_hire, name='delete_hire'),
]
