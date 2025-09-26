# forms.py
from django import forms
from .models import UserProfile
from allauth.account.forms import SignupForm

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'bio', 'image',]
        widgets = {
            "phone_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter US phone number"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
