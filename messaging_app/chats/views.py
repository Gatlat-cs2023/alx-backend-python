from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
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
            # Optionally: return empty queryset or all messages user participates in
            return Message.objects.none()

        # Filter messages by conversation_id and user participation
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            # Return empty queryset if no conversation found
            return Message.objects.none()

        # Check if user is participant, else empty queryset (permissions also enforce 403)
        if user not in conversation.participants.all():
            # Returning empty queryset here, permission class will raise 403 later if needed
            return Message.objects.none()

        # Return messages in that conversation
        return Message.objects.filter(conversation=conversation)
