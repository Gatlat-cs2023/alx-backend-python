from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow users to access their own objects.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participants of a conversation to access messages.
    """

    def has_permission(self, request, view):
        # Allow only authenticated users globally
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Assumes the object (message/conversation) has a participants attribute
        # For a Message, check if request.user is sender or recipient
        return request.user in obj.participants.all() if hasattr(obj, 'participants') else False
