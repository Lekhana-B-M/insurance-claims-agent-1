import re

def preprocess_text(text):
    """Cleans raw PDF text for better AI processing."""
    # Remove multiple newlines and extra spaces
    text = re.sub(r'\s+', ' ', text)
    return text.strip()