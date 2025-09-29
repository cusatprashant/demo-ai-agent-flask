# debug_app.py
from app import create_app
from config import Config
import os

def debug_configuration():
    """Debug the Flask app configuration"""
    print("🔍 Debugging Flask App Configuration...")
    print("=" * 60)
    
    # Check environment variables
    print("📋 Environment Variables:")
    api_key = os.getenv('NVIDIA_DEV_API_KEY')
    secret_key = os.getenv('SECRET_KEY')
    
    print(f"   NVIDIA_DEV_API_KEY: {'✅ Set' if api_key else '❌ Not set'}")
    if api_key:
        print(f"   API Key preview: {'*' * (len(api_key) - 4) + api_key[-4:]}")
    print(f"   SECRET_KEY: {'✅ Set' if secret_key else '❌ Using default'}")
    print()
    
    # Check Flask configuration
    print("⚙️ Flask Configuration:")
    config = Config()
    print(f"   SECRET_KEY: {'✅ Set' if config.SECRET_KEY else '❌ Missing'}")
    print(f"   NVIDIA_API_KEY: {'✅ Set' if config.NVIDIA_API_KEY else '❌ Missing'}")
    print(f"   NVIDIA_BASE_URL: {config.NVIDIA_BASE_URL}")
    print(f"   MODEL_NAME: {config.MODEL_NAME}")
    print()
    
    # Test app creation
    print("🚀 Testing App Creation:")
    try:
        app = create_app()
        print("   ✅ Flask app created successfully")
        
        with app.app_context():
            from app.extensions import openai_client
            if openai_client:
                print("   ✅ OpenAI client initialized successfully")
            else:
                print("   ❌ OpenAI client failed to initialize")
        
        print("   ✅ App context working")
        
        # List routes
        print("\n📍 Registered Routes:")
        for rule in app.url_map.iter_rules():
            print(f"   {rule.methods} {rule.rule} -> {rule.endpoint}")
        
        return app, True
        
    except Exception as e:
        print(f"   ❌ App creation failed: {e}")
        import traceback
        traceback.print_exc()
        return None, False

if __name__ == "__main__":
    app, success = debug_configuration()
    print("=" * 60)
    if success:
        print("🎉 Configuration looks good!")
        print("💡 Try running: python app.py or flask run")
    else:
        print("🚨 Please fix the configuration issues above.")
        print("💡 Make sure to:")
        print("   1. Copy .env.example to .env")
        print("   2. Add your NVIDIA API key")
        print("   3. Install/upgrade OpenAI: pip install openai>=1.0.0")
