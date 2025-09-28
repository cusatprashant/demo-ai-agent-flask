# app/extensions.py
from openai import OpenAI
from flask import current_app

openai_client = None

def init_app(app):
    global openai_client
    try:
        openai_client = OpenAI(
            base_url=app.config['NVIDIA_BASE_URL'],
            api_key=app.config['NVIDIA_API_KEY']
        )
    except Exception as e:
        app.logger.error(f"Failed to initialize OpenAI client: {e}")
        openai_client = None
