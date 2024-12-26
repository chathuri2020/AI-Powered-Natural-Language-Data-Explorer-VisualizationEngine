from django.contrib import admin
from django.urls import path, re_path
from chatbot import views

urlpatterns = [

    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('chat_assistent/', views.chat_assistant,  name='chat_assistant'),  # URL for the chatbot page
    path('send_message/', views.send_message, name='send_message'),
=======
    path('chat_assistant/', views.chat_assistant, name='chat_assistant'),
    path('chatbot/', views.chatbot_index, name='chatbot_index'),
    #path('dashboard/', views.dashbord, name='dashbord'),
    path('', views.index, name='home'),
   # re_path(r'^.*\.*', views.pages, name='pages'),  # Keep this at the end

>>>>>>> chatbot_plot_improvements_chathuri_2024_11_23
]
