from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow users to access their own objects.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to allow only participants of a conversation to
    send (POST), view (GET), update (PUT/PATCH), and delete (DELETE) messages.
    """

    def has_permission(self, request, view):
        # Allow only authenticated users to access any method
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check if user is participant of the conversation/message
        # Adjust this depending on your Message model structure:
        # For example, if Message has sender and recipient fields:

        user = request.user

        is_participant = (user == obj.sender) or (user == obj.recipient)

        # Allow safe methods (GET, HEAD, OPTIONS) for participants
        if request.method in SAFE_METHODS and is_participant:
            return True
        
        # For write methods (POST, PUT, PATCH, DELETE), allow only if participant
        if request.method in ('POST', 'PUT', 'PATCH', 'DELETE') and is_participant:
            return True

        return False
