from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from courses.models import Course

class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question_text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)
    marks = models.IntegerField()

    def __str__(self):
        return self.question_text

class ExamResult(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exam_results')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    date_attempted = models.DateTimeField(auto_now_add=True)
    time_spent = models.IntegerField(null=True, blank=True)  # To store the time spent in the exam
    total_marks = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.student.username} - {self.student.first_name} - {self.student.last_name} - {self.course.title} - {self.score}'