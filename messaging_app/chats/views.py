from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied  # Add this import
from .models import Message, Conversation
from .serializers import MessageSerializer
from .permissions import IsParticipantOfConversation

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        user = self.request.user

        # Get conversation_id from URL query parameters
        conversation_id = self.request.query_params.get('conversation_id')
        if not conversation_id:
            # Return empty queryset if no conversation_id provided
            return Message.objects.none()

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            # Raise 403 Forbidden if conversation does not exist
            raise PermissionDenied(detail="Conversation does not exist or access denied.")

        if user not in conversation.participants.all():
            # Explicitly raise 403 Forbidden if user not participant
            raise PermissionDenied(detail="You do not have permission to access this conversation.")

        # Return messages in that conversation
        return Message.objects.filter(conversation=conversation)
