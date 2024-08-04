

from django.contrib import admin
from .models import Question, Answer, QuizConfig, QuizSettings

class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(QuizConfig)
admin.site.register(QuizSettings)