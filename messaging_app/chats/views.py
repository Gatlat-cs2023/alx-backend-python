from django.shortcuts import render
from .permissions import IsParticipantOfConversation
from rest_framework.permissions import IsAuthenticated

# Create your views here.
from rest_framework import viewsets
from .models import Message
from .serializers import MessageSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]

    # You can override get_queryset to restrict messages to user conversations only
    def get_queryset(self):
        user = self.request.user
        # Assuming Message has sender and recipient
        return Message.objects.filter(sender=user) | Message.objects.filter(recipient=user)
