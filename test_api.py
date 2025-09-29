# test_api.py
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def test_nvidia_api():
    """Test NVIDIA API connection"""
    api_key = os.getenv('NVIDIA_DEV_API_KEY')
    base_url = "https://integrate.api.nvidia.com/v1"
    
    if not api_key:
        print("❌ ERROR: NVIDIA_DEV_API_KEY not found in .env file")
        print("Please:")
        print("1. Copy .env.example to .env")
        print("2. Add your NVIDIA API key from https://build.nvidia.com/explore/discover")
        return False
    
    print(f"✅ API Key found: {'*' * (len(api_key) - 4) + api_key[-4:]}")
    print(f"✅ Base URL: {base_url}")
    
    try:
        client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        
        print("🧪 Testing API connection...")
        response = client.chat.completions.create(
            model="qwen/qwen2.5-coder-32b-instruct",
            messages=[{"role": "user", "content": "Hello! Say hi back."}],
            temperature=0.2,
            max_tokens=50
        )
        
        print("✅ API test successful!")
        print(f"Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing NVIDIA API Setup...")
    print("=" * 50)
    success = test_nvidia_api()
    print("=" * 50)
    if success:
        print("🎉 Setup is working! You can now run your Flask app.")
    else:
        print("🚨 Please fix the issues above before running your Flask app.")
