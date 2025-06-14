from django.db import models

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):  # ✅ Rename this
        return self.filter(receiver=user, read=False).only('id', 'content', 'timestamp', 'sender_id')
