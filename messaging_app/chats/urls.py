from django.urls import path
from .auth import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
]
