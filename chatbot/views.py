from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import chat  


@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_input = data.get('user_input', '')  
        bot_response = process_input(user_input)  
        return JsonResponse({'bot_response': bot_response})
    else:
        return JsonResponse({'error': 'Unsupported method'}, status=400)
from django.shortcuts import render
from django.http import JsonResponse
from . import chat  # Import your chatbot logic
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
def chatbot_html_view(request):
    bot_response = None
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        bot_response = chat.process_input(user_input)  # Replace with your actual chatbot logic

    return render(request, 'supportclaim/chatbot/chatbot.html', {'bot_response': bot_response})
@login_required
def redirect_to_dashboard(request):
    # Assuming the role is stored in request.user.role (or similar)
    user = request.user
    if user.role == 'admin':
        return redirect('support:adminside')  # Change to the actual URL for the admin dashboard
    elif user.role == 'client':
        return redirect('support:clientside')  # Change to the actual URL for the client dashboard
    else:
        return redirect('default_dashboard')  # Default or error handling in case of missing roles