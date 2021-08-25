from django.urls import path
from solver import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('read-image/', views.read_image, name = 'read_image')
]