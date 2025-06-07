from django.urls import path
from .auth import RegisterView
from .views import ConversationListView, MessageListView 

urlpatterns = [
    path('conversations/', ConversationListView.as_view(), name='conversations-list'),
    path('register/', RegisterView.as_view(), name='register'),
]
