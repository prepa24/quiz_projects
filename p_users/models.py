# models.py
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    bio = models.CharField(max_length=500, null=True, blank=True)
    phone_number = PhoneNumberField(region="US", unique=True, null=True, help_text="Enter a US phone number", blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
