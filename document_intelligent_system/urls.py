from django.contrib import admin
from django.urls import path
from chatbot import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat_assistent/', views.chat_assistant),  # URL for the chatbot page
]
