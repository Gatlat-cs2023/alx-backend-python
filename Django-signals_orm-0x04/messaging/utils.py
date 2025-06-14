def get_thread(message):
    """Recursively fetches a message and all of its replies as a nested dict"""
    return {
        "id": message.id,
        "content": message.content,
        "sender": message.sender.username,
        "timestamp": message.timestamp,
        "replies": [
            get_thread(reply)
            for reply in message.replies.all().select_related('sender')
        ]
    }
