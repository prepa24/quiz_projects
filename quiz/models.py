

# Create your models here.
from django.db import models
from PIL import Image



class QuizConfig(models.Model):
    num_questions = models.PositiveIntegerField(default=50)

    def __str__(self):
        return f'Quiz Config (Questions: {self.num_questions})'


class Question(models.Model):
    text = models.CharField(max_length=255)
    image = models.ImageField(upload_to='question_images/', null=True, blank=True)

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            # Get the first ImageSettings object or create one with default values
            settings, created = ImageSettings.objects.get_or_create(
                defaults={'width': 100, 'height': 100}
            )
            img = Image.open(self.image.path)
            img = img.resize((settings.width, settings.height))
            img.save(self.image.path)

    

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
