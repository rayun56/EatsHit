from django.urls import path

from . import views

app_name = 'docmtu'
urlpatterns = [
    path('', views.done, name='done'),
    # path('location/', views.location, name='location'),
    # path('about/', views.about, name='about'),
    # path('dropdown/', views.dropdown, name='dropdown'),
    # path('date/', views.date, name='date')
]
