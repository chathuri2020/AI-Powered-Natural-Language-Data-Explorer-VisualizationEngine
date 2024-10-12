from django.contrib import admin
from django.urls import path, include  # Make sure to include 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chatbot.urls')),  # Include your chatbot app URLs
]
