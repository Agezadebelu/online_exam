from django.shortcuts import render, redirect
#from .forms import UserSignupForm
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login
from .models import User
#from django.contrib.auth.views import LoginView
from courses.models import Course
from exams.models import Question
from exams.models import ExamResult


def home(request):
    return render(request, 'home.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'home.html')


# User Authentication and Role Management.

def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('login_view')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'register.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('admin_dashboard')
            elif user is not None and user.is_teacher:
                login(request, user)
                return redirect('teacher_dashboard')
            elif user is not None and user.is_student:
                login(request, user)
                return redirect('student_dashboard')
            else:
                msg= 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})

# Implement Admin Dashboard

def admin_dashboard(request):
    if not request.user.is_admin:
        return redirect('login')  # Restrict access if not admin

    total_students = User.objects.filter(is_student=True).count()
    total_teachers = User.objects.filter(is_teacher=True).count()
    total_courses = Course.objects.all().count()
    total_questions = Question.objects.all().count()

    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_courses': total_courses,
        'total_questions': total_questions,
    }
    return render(request, 'admin_dashboard.html', context)

def manage_teachers(request):
    if not request.user.is_admin:
        return redirect('login')  # Restrict access if not admin

    teachers = User.objects.filter(is_teacher=True)
    return render(request, 'manage_teachers.html', {'teachers': teachers})

def approve_teacher(request, teacher_id):
    teacher = User.objects.get(id=teacher_id, is_teacher=True)
    teacher.is_active = True  # Approve teacher by activating their account
    teacher.save()
    return redirect('manage_teachers')

def delete_teacher(request, teacher_id):
    teacher = User.objects.get(id=teacher_id, is_teacher=True)
    teacher.delete()
    return redirect('manage_teachers')

def manage_students(request):
    if not request.user.is_admin:
        return redirect('login')  # Restrict access if not admin

    students = User.objects.filter(is_student=True)
    return render(request, 'manage_students.html', {'students': students})

def delete_student(request, student_id):
    student = User.objects.get(id=student_id, is_student=True)
    student.delete()
    return redirect('manage_students')

# Implement Teacher Dashboard
def teacher_dashboard(request):
    if not request.user.is_teacher:
        return redirect('login')  # Restrict access if not teacher

    total_students = User.objects.filter(is_student=True).count()
    total_courses = Course.objects.filter(created_by=request.user).count()  # Courses created by the teacher
    total_questions = Question.objects.filter(course__created_by=request.user).count()  # Questions in the teacher's courses

    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'total_questions': total_questions,
    }
    return render(request, 'teacher_dashboard.html', context)

# Implement Student Dashboard
def student_dashboard(request):
    if not request.user.is_student:
        return redirect('login')  # Restrict access if not student

    total_courses = Course.objects.all().count()
    exam_results = ExamResult.objects.filter(student=request.user)

    context = {
        'total_courses': total_courses,
        'exam_results': exam_results,
    }
    return render(request, 'student_dashboard.html', context)
