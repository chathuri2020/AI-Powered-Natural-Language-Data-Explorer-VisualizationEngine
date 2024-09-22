# views.py
from django.http import JsonResponse
from django.shortcuts import render


def chat_assistant(request):

    from bardapi import Bard
    import os
    import google.generativeai as genai
    genai.configure(api_key="AIzaSyCPBau4ZNNhZ-CiaCdlvNDCG-BxHcjovqc")

# Create the model
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    )

    chat_session = model.start_chat(
    history=[
        {
        "role": "user",
        "parts": [
            "hi\n",
        ],
        },
        {
        "role": "model",
        "parts": [
            "Hi! How can I help you today? \n",
        ],
        },
    ]
    )

    response = chat_session.send_message("what is 1 + 12")
    response = response.text
   # print()

    user_message = request.POST.get('message')



    # Static array of users (not from DB)
    users = ['Hello How Are you']
    #response = 'This is the way you can do that....below has examples..'
    return render(request, 'chatbot/chatbot.html', {'users': users, 'response':response, 'user_message':user_message})


#gggggg