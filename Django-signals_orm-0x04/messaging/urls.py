from django.urls import path
from . import views

urlpatterns = [
    path('history/<int:message_id>/', views.message_history_view, name='message_history'),
]
