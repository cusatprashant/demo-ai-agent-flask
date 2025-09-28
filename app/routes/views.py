# app/routes/views.py
from flask import render_template, request, jsonify, current_app
import openai
from app.routes import main_bp
from app.extensions import openai_client
from app.utils.validators import validate_prompt

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/api/chat', methods=['POST'])
def chat():
    if not openai_client:
        return jsonify({'error': 'AI service not available'}), 503

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400

    prompt = data.get('prompt', '')
    
    # Validate input
    validation_error = validate_prompt(prompt)
    if validation_error:
        return jsonify({'error': validation_error}), 400

    try:
        response = openai_client.chat.completions.create(
            model="qwen/qwen2.5-coder-32b-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        
        return jsonify({
            'response': response.choices[0].message.content.strip()
        })

    except openai.RateLimitError:
        return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429
    except openai.APIConnectionError:
        return jsonify({'error': 'Unable to connect to AI service. Please check your connection.'}), 503
    except openai.APIStatusError as e:
        current_app.logger.error(f"OpenAI API error: {e}")
        return jsonify({'error': f'Service error: {e.message}'}), e.status_code
    except Exception as e:
        current_app.logger.error(f"Unexpected error: {e}")
        return jsonify({'error': 'Service temporarily unavailable'}), 503
