from django.contrib import admin
from django.urls import path, re_path
from chatbot import views

urlpatterns = [

    path('admin/', admin.site.urls),
    path('chat_assistant/', views.chat_assistant, name='chat_assistant'),
    path('chatbot/', views.chatbot_index, name='chatbot_index'),
    #path('dashboard/', views.dashbord, name='dashbord'),
    path('', views.index, name='home'),
   # re_path(r'^.*\.*', views.pages, name='pages'),  # Keep this at the end

]
