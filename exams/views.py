from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Question, ExamResult
from .forms import QuestionForm

# Managing Questions for Admin
def manage_questions(request):
    if not request.user.is_admin:
        return redirect('login')

    questions = Question.objects.all()
    return render(request, 'manage_questions.html', {'questions': questions})

def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_courses')
    else:
        form = QuestionForm()
    return render(request, 'add_question.html', {'form': form})

def delete_question(request, question_id):
    question = Question.objects.get(id=question_id)
    question.delete()
    return redirect('manage_questions')

def edit_question(request, question_id):
    # Logic for editing the question
    question = get_object_or_404(Question, id=question_id)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('manage_questions')  # Redirect to the list of questions after editing
    else:
        form = QuestionForm(instance=question)
    
    return render(request, 'edit_question.html', {'form': form})

def admin_manage_results_view(request):
    results = ExamResult.objects.all()  # Get all results
    return render(request, 'admin_manage_results.html', {'results': results})

# Managing Questions for Teachers

def teacher_manage_questions(request):
    if not request.user.is_teacher:
        return redirect('login')

    questions = Question.objects.filter(course__created_by=request.user)  # Questions for the teacher's courses
    return render(request, 'teacher_manage_questions.html', {'questions': questions})

def teacher_add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            course = form.cleaned_data.get('course')
            if course.created_by == request.user:  # Ensure the teacher owns the course
                question.save()
                return redirect('teacher_manage_questions')
    else:
        form = QuestionForm()
    return render(request, 'teacher_add_question.html', {'form': form})

def teacher_delete_question(request, question_id):
    question = Question.objects.get(id=question_id, course__created_by=request.user)  # Ensure the question belongs to the teacher
    question.delete()
    return redirect('teacher_manage_questions')

def teacher_manage_results_view(request):
    teacher_courses = request.user.course_set.all()  # Get courses managed by this teacher
    results = ExamResult.objects.filter(course__in=teacher_courses)
    return render(request, 'teacher_manage_results.html', {'results': results})

# Managing Questions for Students
def student_take_exam(request, course_id):
    course = Course.objects.get(id=course_id)
    questions = Question.objects.filter(course=course)

    if request.method == 'POST':
        score = 0
        total_marks = 0
        for question in questions:
            selected_option = request.POST.get(str(question.id))
            if selected_option == question.correct_answer:
                score += question.marks  # Assuming `marks` is a field in the `Question` model
        
            total_marks += question.marks

        # Save exam result
        ExamResult.objects.create(student=request.user, course=course, score=score, total_marks=total_marks)
        return redirect('student_exam_results')

    return render(request, 'student_take_exam.html', {'course': course, 'questions': questions})

def student_exam_results_view(request):
    results = ExamResult.objects.filter(student=request.user)
    return render(request, 'student_exam_results.html', {'results': results})
