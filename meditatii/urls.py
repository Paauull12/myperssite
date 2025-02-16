from django.contrib.auth.views import LoginView
from django.urls import path
from django.urls import reverse_lazy

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', LoginView.as_view(
        template_name='meditatii/login.html',
        next_page=reverse_lazy('meditation_list')
    ), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('meditations/', views.meditation_list, name='meditation_list'),
    path('meditations/create/', views.meditation_create, name='meditation_create'),
    path('meditation/<int:meditation_id>/mark-pending/', views.mark_as_pending, name='mark_pending'),
    path('meditation/<int:meditation_id>/mark-paid/', views.mark_as_paid, name='mark_paid'),
    path('student/<str:username>', views.student_details, name='student_details'),

]
