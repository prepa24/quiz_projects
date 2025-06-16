# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('delete-account/', views.delete_account, name='delete_account'),
]
