from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('api/students/', views.api_students, name='api_students'),
    path('api/students/<int:student_id>/', views.api_student_detail, name='api_student_detail'),
]
