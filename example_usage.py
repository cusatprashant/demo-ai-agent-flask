# example_usage.py - How to use the formatted responses

import requests
import json

# Example API calls with different formatting options

BASE_URL = "http://localhost:5000"

def test_formatting_options():
    """Test different formatting options"""
    
    test_prompt = """
    Write a Python function that calculates fibonacci numbers. 
    Please include:
    1. The function code
    2. An example of how to use it
    3. Explanation of the algorithm
    """
    
    # Test different format types
    format_types = ['enhanced_text', 'html', 'text', 'quick', 'raw']
    
    for format_type in format_types:
        print(f"\n{'='*50}")
        print(f"Testing format: {format_type}")
        print(f"{'='*50}")
        
        payload = {
            "prompt": test_prompt,
            "format": format_type
        }
        
        try:
            response = requests.post(f"{BASE_URL}/api/chat", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Success with format: {data['format_used']}")
                print(f"Response length: {len(data['response'])} chars")
                print(f"\nFormatted Response:")
                print("-" * 30)
                print(data['response'][:500] + "..." if len(data['response']) > 500 else data['response'])
                
                if format_type != 'raw':
                    print(f"\nRaw Response (first 200 chars):")
                    print("-" * 30)
                    print(data['raw_response'][:200] + "..." if len(data['raw_response']) > 200 else data['raw_response'])
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error: {e}")

def test_simple_formatting():
    """Test simple question with formatting"""
    
    payload = {
        "prompt": "What is machine learning? Give me a brief explanation.",
        "format": "enhanced_text"
    }
    
    response = requests.post(f"{BASE_URL}/api/chat", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Simple formatting test successful!")
        print(f"Formatted response:\n{data['response']}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    print("🧪 Testing Response Formatting Options")
    print("Make sure your Flask app is running on http://localhost:5000")
    print()
    
    # Test simple formatting first
    test_simple_formatting()
    
    # Test all formatting options
    test_formatting_options()
