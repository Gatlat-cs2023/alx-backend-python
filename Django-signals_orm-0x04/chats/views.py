from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

@cache_page(60)  # cache timeout in seconds
@login_required
def conversation_messages_view(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id).order_by('timestamp')
    # your code to render messages or return JsonResponse
