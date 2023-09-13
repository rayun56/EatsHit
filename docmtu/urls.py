from django.urls import path

from . import views

app_name = 'docmtu'
urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('location/', views.location, name='location'),
    path('about/', views.about, name='about'),
    path('dropdown/', views.dropdown, name='dropdown'),
    path('date/', views.date, name='date')
]
