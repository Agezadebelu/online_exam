from django import forms
from .models import Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['course', 'question_text', 'option1', 'option2', 'option3', 'option4', 'correct_answer', 'marks']