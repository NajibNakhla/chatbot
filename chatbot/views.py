from django.shortcuts import render
import json
from django.http import JsonResponse
from .chatbot import predict_class, get_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

def chatbot_endpoint(request):
    intents_json = json.loads(open('chatbot/intents.json').read())
    
    if request.method == 'POST':
        message = request.POST.get('message')

        # Get intents and response from chatbot
        intents = predict_class(message)
        response = get_response(intents, intents_json)

        return JsonResponse({'response': response})
    
    elif request.method == 'OPTIONS':
        # Respond to CORS preflight request
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'  # Update with your allowed origin
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'  # Update with allowed methods
        response['Access-Control-Allow-Headers'] = 'Content-Type'  # Update with allowed headers
        return response
    
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)