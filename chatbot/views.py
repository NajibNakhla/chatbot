from django.shortcuts import render
import json
from django.http import JsonResponse
from .chatbot import predict_class, get_response

def chatbot_endpoint(request):
    intents_json = json.loads(open('chatbot/intents.json').read())
    if request.method == 'POST':
        message = request.POST.get('message')  # Assuming the user's message is sent as a POST parameter named 'message'

        # Get intents and response from chatbot
        intents = predict_class(message)
        response = get_response(intents, intents_json)


        return JsonResponse({'response': response})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
