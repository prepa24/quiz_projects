

# Create your models here.
from django.db import models
from PIL import Image
from django_resized import ResizedImageField



class QuizConfig(models.Model):
    num_questions = models.PositiveIntegerField(default=50)

    def __str__(self):
        return f'Quiz Config (Questions: {self.num_questions})'


class Question(models.Model):
    text = models.CharField(max_length=255)
    #image = models.ImageField(upload_to='question_images/', null=True, blank=True)
    image1 = ResizedImageField(size=[100, 100], upload_to='question_images', null=True, blank=True)

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

class ImageSettings(models.Model):
    width = models.PositiveIntegerField(default=100)
    height = models.PositiveIntegerField(default=100)

    def __str__(self):
        return f"Image Size: {self.width}x{self.height}"
