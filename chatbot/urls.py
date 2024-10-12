from django.contrib import admin
from django.urls import path
from chatbot import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat_assistent/', views.chat_assistant,  name='chat_assistant'),  # URL for the chatbot page
   # path('send_message/', views.send_message, name='send_message'),

    path('up/<int:f_oid>', views.updateView, name= 'update_url'),
]
