from django.contrib import admin
from .models import QuizHistory, QuizConfig, Question, Answer, QuizSettings, ImageSettings
from parler.admin import TranslatableAdmin, TranslatableTabularInline

class AnswerAdmin(TranslatableTabularInline):
    model = Answer

@admin.register(QuizHistory)
class QuizHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_taken', 'passed', 'correct_answers', 'incorrect_answers', 'total_time_seconds')
    list_filter = ('user', 'passed', 'date_taken')
    search_fields = ('user__username',)

@admin.register(QuizConfig)
class QuizConfigAdmin(admin.ModelAdmin):
    list_display = ('num_questions',)

@admin.register(Question)
class QuestionAdmin(TranslatableAdmin):
    #list_display = ('text',)
    #search_fields = ('translations__text',)
    inlines = [AnswerAdmin]

#@admin.register(Answer)

    #list_display = ('question', 'text', 'is_correct')
    #search_fields = ('translations__text',)
    #list_filter = ('is_correct',)

@admin.register(QuizSettings)
class QuizSettingsAdmin(admin.ModelAdmin):
    list_display = ('time_limit',)

@admin.register(ImageSettings)
class ImageSettingsAdmin(admin.ModelAdmin):
    list_display = ('width', 'height')
