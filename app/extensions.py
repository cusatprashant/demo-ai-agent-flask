# app/extensions.py

import os
from openai import OpenAI
from flask import current_app

openai_client = None

def init_app(app):
    global openai_client
    try:
        # Get API key from config
        api_key = app.config.get('NVIDIA_API_KEY')
        base_url = app.config.get('NVIDIA_BASE_URL')
        
        if not api_key:
            app.logger.error("NVIDIA_API_KEY not found in configuration")
            openai_client = None
            return
            
        print(f"Initializing OpenAI client with API key: {'*' * (len(api_key) - 4) + api_key[-4:] if api_key else 'None'}")
        print(f"Using base URL: {base_url}")
        
        # Initialize OpenAI client with modern v1.x syntax
        openai_client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        
        # Optional: Set proxy via environment variables
        proxy = app.config.get('NVIDIA_PROXY')
        if proxy:
            os.environ['HTTP_PROXY'] = proxy
            os.environ['HTTPS_PROXY'] = proxy
            print(f"Using proxy: {proxy}")

    except Exception as e:
        app.logger.error(f"Failed to initialize OpenAI client: {e}")
        openai_client = None