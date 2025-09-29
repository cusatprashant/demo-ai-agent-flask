# app/utils/response_formatter.py
import re
import html

def format_ai_response(raw_content, format_type='enhanced_text'):
    """
    Format AI response for better user readability
    
    Args:
        raw_content: Raw response from AI
        format_type: 'text', 'html', 'enhanced_text'
    
    Returns:
        Formatted response string
    """
    if not raw_content:
        return ""
    
    content = raw_content.strip()
    
    if format_type == 'html':
        return _format_html(content)
    elif format_type == 'enhanced_text':
        return _format_enhanced_text(content)
    else:
        return _format_plain_text(content)

def _format_plain_text(content):
    """Basic text cleanup"""
    # Fix multiple newlines
    formatted = re.sub(r'\n{3,}', '\n\n', content)
    
    # Ensure consistent spacing
    formatted = re.sub(r'[ \t]+', ' ', formatted)
    
    return formatted.strip()

def _format_enhanced_text(content):
    """Enhanced text formatting with better structure"""
    # Split into sections
    sections = content.split('\n\n')
    formatted_sections = []
    
    for section in sections:
        section = section.strip()
        if not section:
            continue
            
        # Handle different section types
        if section.startswith('```'):
            # Code block - preserve formatting
            formatted_sections.append(section)
        elif section.startswith('#'):
            # Header - ensure spacing
            formatted_sections.append(section)
        elif section.startswith(('- ', '* ', '1. ', '2. ', '3. ')):
            # List - clean up spacing
            lines = section.split('\n')
            clean_lines = [line.strip() for line in lines if line.strip()]
            formatted_sections.append('\n'.join(clean_lines))
        else:
            # Regular paragraph - clean up line breaks within
            cleaned = ' '.join(section.split())
            if cleaned:
                formatted_sections.append(cleaned)
    
    return '\n\n'.join(formatted_sections)

def _format_html(content):
    """Format for HTML display"""
    # Escape HTML first
    formatted = html.escape(content)
    
    # Handle code blocks
    def replace_code_block(match):
        lang = match.group(1) or ''
        code = match.group(2).strip()
        return f'<pre><code class="language-{lang}">{html.escape(code)}</code></pre>'
    
    formatted = re.sub(r'```(\w+)?\n?(.*?)```', replace_code_block, formatted, flags=re.DOTALL)
    
    # Handle paragraphs
    paragraphs = formatted.split('\n\n')
    html_paragraphs = []
    
    for para in paragraphs:
        para = para.strip()
        if not para or para.startswith('<pre>'):
            html_paragraphs.append(para)
            continue
            
        # Handle headers
        if para.startswith('#'):
            level = len(para) - len(para.lstrip('#'))
            text = para.lstrip('# ').strip()
            html_paragraphs.append(f'<h{min(level, 6)}>{text}</h{min(level, 6)}>')
            continue
            
        # Handle lists
        if para.startswith(('- ', '* ')):
            items = para.split('\n')
            list_items = [f'<li>{item[2:].strip()}</li>' for item in items if item.strip().startswith(('- ', '* '))]
            html_paragraphs.append(f'<ul>{"".join(list_items)}</ul>')
            continue
            
        if re.match(r'^\d+\. ', para):
            items = para.split('\n')
            list_items = [f'<li>{re.sub(r"^\\d+\\. ", "", item).strip()}</li>' for item in items if re.match(r'^\\d+\\. ', item.strip())]
            html_paragraphs.append(f'<ol>{"".join(list_items)}</ol>')
            continue
            
        # Regular paragraph
        para = para.replace('\n', '<br>')
        html_paragraphs.append(f'<p>{para}</p>')
    
    # Handle inline code
    formatted = '\n'.join(html_paragraphs)
    formatted = re.sub(r'`([^`]+)`', r'<code>\1</code>', formatted)
    
    return formatted

# Quick formatting functions for common use cases
def quick_format_response(content):
    """Quick and simple formatting for immediate use"""
    if not content:
        return ""
        
    # Basic cleanup
    formatted = content.strip()
    
    # Fix paragraph spacing
    formatted = re.sub(r'\n{3,}', '\n\n', formatted)
    
    # Clean up code blocks
    formatted = re.sub(r'```(\w+)?\n(.*?)```', lambda m: f'```{m.group(1) or ""}\n{m.group(2).strip()}\n```', formatted, flags=re.DOTALL)
    
    return formatted

def format_response_markdown(content):
    """Format response with markdown-style improvements"""
    formatted = content.strip()
    
    # Add proper spacing around headers
    formatted = re.sub(r'^(#{1,6})\s*(.+)$', r'\1 \2\n', formatted, flags=re.MULTILINE)
    
    # Ensure paragraphs are separated
    formatted = re.sub(r'\n{3,}', '\n\n', formatted)
    
    # Format lists properly
    formatted = re.sub(r'^([*-])\s*(.+)$', r'\1 \2', formatted, flags=re.MULTILINE)
    
    return formatted


