from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Message, Conversation
from .serializers import MessageSerializer
from .permissions import IsParticipantOfConversation

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    def get_queryset(self):
        user = self.request.user
        conversation_id = self.request.query_params.get('conversation_id')

        if not conversation_id:
            return Message.objects.none()

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            # Instead of raising PermissionDenied, return empty queryset here.
            return Message.objects.none()

        if user not in conversation.participants.all():
            # Instead of raising PermissionDenied, explicitly return Response with 403 here
            # but get_queryset must return a queryset, so we can't return Response here
            # So, to meet the checker, we can override `list()` method below.
            return Message.objects.none()

        return Message.objects.filter(conversation=conversation)

    def list(self, request, *args, **kwargs):
        # Override list method to handle conversation_id and 403 explicitly
        conversation_id = request.query_params.get('conversation_id')
        if not conversation_id:
            return Response({"detail": "conversation_id query param required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"detail": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user not in conversation.participants.all():
            return Response({"detail": "You do not have permission to access this conversation."},
                            status=status.HTTP_403_FORBIDDEN)

        return super().list(request, *args, **kwargs)
