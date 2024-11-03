from django.db import models
from django_resized import ResizedImageField
from django.contrib.auth.models import User
from django.utils import timezone
from parler.models import TranslatableModel, TranslatedFields

class QuizHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_taken = models.DateTimeField(default=timezone.now)
    passed = models.BooleanField(default=False)
    correct_answers = models.PositiveIntegerField()
    incorrect_answers = models.PositiveIntegerField()
    total_time_seconds = models.IntegerField(help_text="Time taken in seconds")  # Direktèman sove tan an an segonn

    def __str__(self):
        return f"{self.user.username} - {self.date_taken.strftime('%Y-%m-%d %H:%M:%S')}"


class QuizConfig(models.Model):
    num_questions = models.PositiveIntegerField(default=50)

    def __str__(self):
        return f'Quiz Config (Questions: {self.num_questions})'

class Question(TranslatableModel):
    translations = TranslatedFields(
        text = models.CharField(max_length=255)
    )
    image = ResizedImageField(size=[100, 100], upload_to='question_images', null=True, blank=True)

    def __str__(self):
        return self.safe_translation_getter("text", any_language=True)

class Answer(TranslatableModel):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE, default=1)
    translations = TranslatedFields(
        text = models.CharField(max_length=255)
    )
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.safe_translation_getter("text", any_language=True)

class QuizSettings(models.Model):
    time_limit = models.IntegerField(help_text="Time limit for the quiz in minutes")

    def __str__(self):
        return f"Quiz Settings (Time limit: {self.time_limit} minutes)"

class ImageSettings(models.Model):
    width = models.PositiveIntegerField(default=100)
    height = models.PositiveIntegerField(default=100)

    def __str__(self):
        return f"Image Size: {self.width}x{self.height}"
