from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import JsonResponse
from .models import Message
from .utils import get_thread  # if you placed it in a utils file


@login_required
def delete_user(request):
    user = request.user
    user.delete()
    messages.success(request, "Your account has been deleted.")
    return redirect('home')  # Replace 'home' with your homepage route name

def threaded_conversations_view(request):
    top_level_messages = Message.objects.filter(parent_message__isnull=True)\
        .select_related('sender')\
        .prefetch_related('replies__sender')

    threads = [get_thread(msg) for msg in top_level_messages]

    return JsonResponse({"threads": threads}, safe=False)
