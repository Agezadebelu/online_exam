from django.shortcuts import render, redirect
from .models import Course
from .forms import CourseForm

# Managing Courses for Admin

def manage_courses(request):
    #if not request.user.is_admin:
    #    return redirect('login')

    courses = Course.objects.all()
    return render(request, 'manage_courses.html', {'courses': courses})

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_courses')
    else:
        form = CourseForm()
    return render(request, 'add_course.html', {'form': form})

def delete_course(request, course_id):
    course = Course.objects.get(id=course_id)
    course.delete()
    return redirect('manage_courses')

# Managing Courses for Teachers

def teacher_manage_courses(request):
    #if not request.user.is_teacher:
    #    return redirect('login')  # Restrict access if not teacher

    courses = Course.objects.filter(created_by=request.user)  # Only show courses created by the teacher
    return render(request, 'teacher_manage_courses.html', {'courses': courses})

def teacher_add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.created_by = request.user  # Associate course with the teacher
            course.save()
            return redirect('teacher_manage_courses')
    else:
        form = CourseForm()
    return render(request, 'teacher_add_course.html', {'form': form})

def teacher_delete_course(request, course_id):
    course = Course.objects.get(id=course_id, created_by=request.user)  # Ensure the course belongs to the teacher
    course.delete()
    return redirect('teacher_manage_courses')

# Managing Courses for Students
def student_view_courses(request):
    courses = Course.objects.all()
    return render(request, 'student_view_courses.html', {'courses': courses})
