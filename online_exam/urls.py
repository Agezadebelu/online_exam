"""online_exam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from users import views as user_views
from courses import views as course_views
from exams import views as exam_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.home, name='home'),  # Home page URL
    path('contact/', user_views.contact, name='contact'),
    path('about/', user_views.about, name='about'),

    path('login/', user_views.login_view, name='login_view'),
    path('register/', user_views.register, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Admin dashboard and management URLs
    path('admin/dashboard/', user_views.admin_dashboard, name='admin_dashboard'),
    path('admin/teachers/', user_views.manage_teachers, name='manage_teachers'),
    path('admin/teachers/approve/<int:teacher_id>/', user_views.approve_teacher, name='approve_teacher'),
    path('admin/teachers/delete/<int:teacher_id>/', user_views.delete_teacher, name='delete_teacher'),
    path('admin/students/', user_views.manage_students, name='manage_students'),
    path('admin/students/delete/<int:student_id>/', user_views.delete_student, name='delete_student'),
    
    # Courses management
    path('admin/courses/', course_views.manage_courses, name='manage_courses'),
    path('admin/courses/add/', course_views.add_course, name='add_course'),
    path('admin/courses/delete/<int:course_id>/', course_views.delete_course, name='delete_course'),

    # questions management
    path('admin/questions/', exam_views.manage_questions, name='manage_questions'),
    path('admin/questions/add/', exam_views.add_question, name='add_question'),
    path('admin/questions/delete/<int:question_id>/', exam_views.delete_question, name='delete_question'),
    path('admin/questions/edit/<int:question_id>/', exam_views.edit_question, name='edit_question'),

    # Teacher dashboard and management URLs
    path('teacher/dashboard/', user_views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/courses/', course_views.teacher_manage_courses, name='teacher_manage_courses'),
    path('teacher/courses/add/', course_views.teacher_add_course, name='teacher_add_course'),
    path('teacher/courses/delete/<int:course_id>/', course_views.teacher_delete_course, name='teacher_delete_course'),
    
    # Teacher questions management
    path('teacher/questions/', exam_views.teacher_manage_questions, name='teacher_manage_questions'),
    path('teacher/questions/add/', exam_views.teacher_add_question, name='teacher_add_question'),
    path('teacher/questions/delete/<int:question_id>/', exam_views.teacher_delete_question, name='teacher_delete_question'),

    # Student dashboard and exam URLs
    path('student/dashboard/', user_views.student_dashboard, name='student_dashboard'),
    path('student/courses/', course_views.student_view_courses, name='student_view_courses'),
    path('student/exam/<int:course_id>/', exam_views.student_take_exam, name='student_take_exam'),
]