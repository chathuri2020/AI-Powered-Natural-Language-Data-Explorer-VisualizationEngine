from django.contrib import admin
from django.urls import path, re_path
from chatbot import views

urlpatterns = [

    path('admin/', admin.site.urls),
    path('chat_assistant/', views.chat_assistant, name='chat_assistant'),
    # This must be 'chat_assistant'  # URL for the chatbot page
    path('chat_assistant/', views.chatbot_index, name='chatbot_index'),
    # path('send_message/', views.send_message, name='send_message'),
    # path('up/<int:f_oid>', views.updateView, name='update_url'),

    # The home page
    path('', views.index, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
