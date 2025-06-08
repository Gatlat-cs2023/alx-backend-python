import logging
from datetime import datetime
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logging.basicConfig(
            filename='requests.log',
            level=logging.INFO,
            format='%(message)s'
        )

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)

        return self.get_response(request)

# Django-Middleware-0x03/chats/middleware.py

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # Allow only between 18:00 (6 PM) and 21:00 (9 PM)
        if current_hour < 18 or current_hour >= 21:
            return HttpResponseForbidden("Access to chat is only allowed between 6 PM and 9 PM.")

        return self.get_response(request)
