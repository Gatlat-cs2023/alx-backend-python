from django.contrib import admin
from django.urls import path, include  # Import include to include app URLs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),  # Include the URLs from the chats app
]
