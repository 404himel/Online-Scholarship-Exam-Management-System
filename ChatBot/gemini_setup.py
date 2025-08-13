import logging
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)

# Load environment variables
try:
    load_dotenv()
    logging.info("Loaded environment variables from .env file.")
except Exception as e:
    logging.error(f"Error loading .env file: {e}")

# Configure the Google Generative AI API
try:
    api_key = os.getenv("gemini_api_key")
    if not api_key:
        logging.error("GOOGLE_API_KEY not found in environment variables.")
    else:
        genai.configure(api_key=api_key)
        logging.info("Google Generative AI API configured.")
except Exception as e:
    logging.error(f"Error configuring Google Generative AI API: {e}")


def get_gemini_response(prompt):
    """Send a prompt to Gemini API and return the response text."""
    try:
        model = genai.GenerativeModel("gemini-2.5-pro")
        response = model.generate_content(prompt)

        # Safely extract text
        if hasattr(response, "text") and response.text:
            text_output = response.text.strip()
        elif hasattr(response, "candidates") and response.candidates:
            text_output = response.candidates[0].content.parts[0].text.strip()
        else:
            text_output = "No response text received."

        logging.info(f"Gemini response: {text_output}")
        return text_output

    except Exception as e:
        logging.error(f"Error in get_gemini_response(): {e}")
        return "Sorry, I couldn't process that."
