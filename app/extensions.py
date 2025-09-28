# app/extensions.py

import os
import openai
from flask import current_app

openai_client = None

def init_app(app):
    global openai_client
    try:
        # Set OpenAI configuration globally
        openai.api_key = app.config['NVIDIA_API_KEY']
        openai.base_url = app.config['NVIDIA_BASE_URL']

        # Optional: Set proxy via environment variables if needed
        if 'NVIDIA_PROXY' in app.config:
            os.environ['HTTP_PROXY'] = app.config['NVIDIA_PROXY']
            os.environ['HTTPS_PROXY'] = app.config['NVIDIA_PROXY']

        # Assign the openai module itself as the client
        openai_client = openai

    except Exception as e:
        app.logger.error(f"Failed to initialize OpenAI client: {e}")
        openai_client = None