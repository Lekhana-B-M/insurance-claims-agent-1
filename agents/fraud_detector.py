from config.routing_config import FRAUD_KEYWORDS

def check_for_fraud(description):
    """
    Scans description for suspicious keywords.
    """
    desc_lower = str(description).lower()
    found_keywords = [word for word in FRAUD_KEYWORDS if word in desc_lower]
    
    return len(found_keywords) > 0, found_keywords