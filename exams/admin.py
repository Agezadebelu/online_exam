from django.contrib import admin
from .models import Question
from .models import ExamResult

# Register your models here.
admin.site.register(Question)
admin.site.register(ExamResult)
