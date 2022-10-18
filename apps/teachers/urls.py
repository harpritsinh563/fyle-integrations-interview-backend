from django.urls import path

from apps.teachers.views import TeacherAssignmentView


urlpatterns = [
    path('assignments/',TeacherAssignmentView.as_view(), name='teachers-assignments')
]
