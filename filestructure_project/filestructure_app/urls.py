from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('process/', views.process_files, name='process_files'),
    path('result/<str:session_id>/', views.result, name='result'),
]