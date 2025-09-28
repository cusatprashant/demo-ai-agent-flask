# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    NVIDIA_API_KEY = os.environ.get('NVIDIA_DEV_API_KEY')
    NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
    MODEL_NAME = "qwen/qwen3-coder-480b-a35b-instruct"