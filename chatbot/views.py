# views.py
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse

def chatbot_index(request):
    return render(request, 'chatbot/chatbot.html')


def chat_assistant(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        # Process the message...
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

        response = chat_session.send_message(message)

        if response:
            response_text = response.text  # Assuming response.text holds the actual response
        else:
            response_text = "Sorry, I couldn't understand your query."

        response = "Your response here"  # Generate a response based on the input
        return JsonResponse({'response': response_text})

    # Handle GET requests by rendering the chatbot page
