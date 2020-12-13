from django.urls import path
from . import views


urlpatterns = [
    path('student_detail/', views.get_student.as_view(), name='get_student'),
    path('update_subject/', views.UpdateSubjectView.as_view(),name='update_subject')
]