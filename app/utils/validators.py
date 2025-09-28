# app/utils/validators.py
def validate_prompt(prompt):
    """Validate user prompt input"""
    if not prompt or not prompt.strip():
        return "Prompt cannot be empty"
    
    if not isinstance(prompt, str):
        return "Prompt must be text"
    
    if len(prompt.strip()) < 3:
        return "Prompt too short (minimum 3 characters)"
    
    if len(prompt) > 2000:
        return "Prompt too long (maximum 2000 characters)"
    
    return None
