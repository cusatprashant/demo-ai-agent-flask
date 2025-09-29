# app/routes/views.py
from flask import render_template, request, jsonify, current_app
from openai import RateLimitError, APIConnectionError, APIStatusError
from app.routes import main_bp
from app.extensions import openai_client
from app.utils.validators import validate_prompt
from app.utils.response_formatter import format_ai_response, quick_format_response

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
    print(f"Received prompt: {prompt}")
    
    # Validate input
    validation_error = validate_prompt(prompt)
    if validation_error:
        return jsonify({'error': validation_error}), 400
    try:
        response = openai_client.chat.completions.create(
            model=current_app.config.get('MODEL_NAME', 'qwen/qwen2.5-coder-32b-instruct'),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            top_p=0.7,
            max_tokens=1024,
            stream=False
        )
        
        # Get raw response
        raw_content = response.choices[0].message.content
        
        # Get format preference from request (default to enhanced_text)
        format_type = data.get('format', 'enhanced_text')
        
        # Format the response for better readability
        if format_type == 'raw':
            formatted_content = raw_content
        elif format_type == 'quick':
            formatted_content = quick_format_response(raw_content)
        else:
            formatted_content = format_ai_response(raw_content, format_type)
        
        return jsonify({
            'response': formatted_content,
            'raw_response': raw_content,  # Include raw for debugging
            'format_used': format_type,
            'success': True
        })

    except RateLimitError:
        return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429
    except APIConnectionError:
        return jsonify({'error': 'Unable to connect to AI service. Please check your connection.'}), 503
    except APIStatusError as e:
        current_app.logger.error(f"OpenAI API error: {e}")
        return jsonify({'error': f'Service error: {str(e)}'}), getattr(e, 'status_code', 500)
    except Exception as e:
        current_app.logger.error(f"Unexpected error: {e}")
        return jsonify({'error': 'Service temporarily unavailable'}), 503
