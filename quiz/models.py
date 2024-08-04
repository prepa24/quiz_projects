

# Create your models here.
from django.db import models

from django.db import models

class QuizConfig(models.Model):
    num_questions = models.PositiveIntegerField(default=50)

    def __str__(self):
        return f'Quiz Config (Questions: {self.num_questions})'


class Question(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    
class QuizSettings(models.Model):
    time_limit = models.IntegerField(help_text="Time limit for the quiz in minutes")

    def __str__(self):
        return f"Quiz Settings (Time limit: {self.time_limit} minutes)"
