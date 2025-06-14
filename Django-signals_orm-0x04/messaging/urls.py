from django.urls import path
from . import views
from .views import unread_messages_view

urlpatterns = [
    path('send/', views.send_message, name='send_message'),
]

urlpatterns = [
    path('unread/', unread_messages_view, name='unread_messages'),
]
