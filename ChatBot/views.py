from django.shortcuts import render
from django.http import JsonResponse
import logging
from .gemini_setup import get_gemini_response

logging.basicConfig(level=logging.INFO)

def index(request):
    logging.info("Rendering chatbot page.")
    return render(request, "chatbot/index.html")

def chat(request):
    if request.method == "POST":
        try:
            user_message = request.POST.get("message", "")
            logging.info(f"User message: {user_message}")
            bot_reply = get_gemini_response(user_message)
            return JsonResponse({"response": bot_reply})
        except Exception as e:
            logging.error(f"Error in chat(): {e}")
            return JsonResponse({"response": "An error occurred."})
    return JsonResponse({"error": "Invalid request method."}, status=405)
