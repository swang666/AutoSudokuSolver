from django.urls import path
from solver import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('read-image/', views.read_image, name = 'read_image'),
    path('process-image/', views.process_image, name = 'process_image'),
    path('render-output/', views.render_output, name = 'render_output')
]