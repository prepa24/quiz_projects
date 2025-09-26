# forms.py
from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'bio', 'image',]
        widgets = {
            "phone_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter US phone number"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
