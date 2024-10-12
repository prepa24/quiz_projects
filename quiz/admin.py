

from django.contrib import admin
from .models import ImageSettings, Question, Answer, QuizConfig, QuizSettings, QuizHistory

class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(QuizConfig)
admin.site.register(QuizSettings)
admin.site.register(ImageSettings)
admin.site.register(QuizHistory)