# app.py
import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure OpenAI API key
client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = os.getenv("NVIDIA_DEV_API_KEY")
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_prompt():
    try:
        user_input = request.form['prompt']
        
        if not user_input.strip():
            return jsonify({'response': 'Please enter a valid prompt.'}), 400
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="qwen/qwen2.5-coder-32b-instruct",  # or "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a helpful agentic AI assistant."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=1024,
            temperature=0.2
        )
        
        ai_response = response.choices[0].message['content'].strip()
        return jsonify({'response': ai_response})
    
    except OpenAI.error.AuthenticationError:
        return jsonify({'response': 'Authentication error. Please check your API key.'}), 401
    except OpenAI.error.RateLimitError:
        return jsonify({'response': 'Rate limit exceeded. Please try again later.'}), 429
    except Exception as e:
        return jsonify({'response': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
