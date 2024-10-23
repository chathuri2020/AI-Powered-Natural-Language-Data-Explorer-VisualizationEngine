import mysql.connector
from django.http import JsonResponse
from django.shortcuts import render


def chatbot_index(request):
    # Loads the initial chatbot page
    return render(request, 'chatbot/chatbot.html')


def chat_assistant(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        from bardapi import Bard
        import google.generativeai as genai
        genai.configure(api_key="AIzaSyCPBau4ZNNhZ-CiaCdlvNDCG-BxHcjovqc")


# SQL Implementation
        import mysql.connector

        # Create the model
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
        }

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )

        chat_session = model.start_chat(
            history=[
                {"role": "user", "parts": ["hi\n"]},
                {"role": "model", "parts": [
                    "Hi! How can I help you today?\n"]},
            ]
        )
        response = chat_session.send_message(message)
        response_text = response.text if response else "Sorry, I couldn't understand your query."
        return JsonResponse({'response': response_text})

    return render(request, 'chatbot/chatbot.html')
