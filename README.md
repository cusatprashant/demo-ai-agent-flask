# Demo AI Agent Flask App

A Flask web application that integrates with NVIDIA's API for AI chat functionality.

## 🚨 Fixing the 404 Error

The "ERROR in views: OpenAI API error: Error code: 404" was caused by several issues:

### Issues Fixed:
1. **OpenAI SDK Version Mismatch** - Updated from legacy v0.x to modern v1.x+ syntax
2. **Missing API Key Configuration** - Added proper error handling for missing API keys
3. **Incorrect Exception Handling** - Fixed import statements for OpenAI exceptions
4. **Model Configuration** - Standardized model name across files

## 🛠️ Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your NVIDIA API key
NVIDIA_DEV_API_KEY=your_actual_api_key_here
```

### 3. Test Your Setup
```bash
# Test API connection
python test_api.py

# Debug configuration
python debug_app.py
```

### 4. Run the Application
```bash
python run.py
```

## 🔍 Troubleshooting

### If you get a 404 error:

1. **Check API Key:**
   ```bash
   python test_api.py
   ```

2. **Verify Configuration:**
   ```bash
   python debug_app.py
   ```

3. **Common Issues:**
   - Missing `.env` file → Copy `.env.example` to `.env`
   - Empty API key → Add your NVIDIA API key to `.env`
   - Wrong OpenAI version → Run `pip install openai>=1.0.0`
   - Model not available → Check NVIDIA's available models

### If the model doesn't exist:
Update `MODEL_NAME` in `config.py` to a valid model from NVIDIA's catalog:
- `qwen/qwen2.5-coder-32b-instruct`
- `nvidia/llama-3.1-nemotron-70b-instruct`
- `microsoft/phi-3-mini-128k-instruct`

## 📁 Project Structure
```
Demo_AI_Agent/
├── app/
│   ├── __init__.py
│   ├── extensions.py          # OpenAI client initialization
│   ├── routes/
│   │   ├── views.py          # Main chat endpoint
│   │   └── __init__.py
│   ├── utils/
│   │   └── validators.py     # Input validation
│   ├── templates/
│   └── static/
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── run.py                   # Application entry point
├── test_api.py              # API connection tester
├── debug_app.py             # Configuration debugger
├── .env.example             # Environment template
└── README.md
```

## 🔧 Code Changes Made

### 1. Fixed `app/extensions.py`:
- Updated to use modern OpenAI v1.x client initialization
- Added proper error handling for missing API keys
- Improved logging for debugging

### 2. Fixed `app/routes/views.py`:
- Updated exception imports
- Fixed response parsing to use `.content`
- Improved error handling

### 3. Updated `requirements.txt`:
- Specified minimum versions
- Ensured OpenAI v1.x compatibility

### 4. Fixed `config.py`:
- Standardized model name

## 🌐 API Endpoints

- `GET /` - Main chat interface
- `POST /api/chat` - Chat with AI
  ```json
  {
    "prompt": "Your message here"
  }
  ```

## 🎯 Usage Example

```python
import requests

response = requests.post('http://localhost:5000/api/chat', json={
    'prompt': 'Hello, how are you?'
})

print(response.json())
```

## 📝 Notes

- This app uses NVIDIA's API endpoints compatible with OpenAI's interface
- Rate limits and error handling are implemented
- Input validation prevents malformed requests
- Debug tools included for easier troubleshooting
