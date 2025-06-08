import logging
from datetime import datetime
from django.http import HttpResponseForbidden
import time
from collections import defaultdict
from django.http import HttpResponseTooManyRequests
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
# Django-Middleware-0x03/chats/middleware.py

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Tracks IP -> [timestamps]
        self.message_log = defaultdict(list)

    def __call__(self, request):
        if request.method == "POST":
            ip = self.get_client_ip(request)
            current_time = time.time()

            # Remove timestamps older than 60 seconds
            self.message_log[ip] = [
                t for t in self.message_log[ip] if current_time - t < 60
            ]

            if len(self.message_log[ip]) >= 5:
                return HttpResponseTooManyRequests(
                    "Rate limit exceeded. Max 5 messages per minute."
                )

            self.message_log[ip].append(current_time)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
# Django-Middleware-0x03/chats/middleware.py

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        # Skip if user is not authenticated (optional)
        if not user.is_authenticated:
            return HttpResponseForbidden("Authentication required.")

        # Only allow admins and moderators
        if not user.is_superuser and not user.groups.filter(name__in=["moderator"]).exists():
            return HttpResponseForbidden("Access denied. Admin or moderator role required.")

        return self.get_response(request)
