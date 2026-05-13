import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def determine_route(extracted_fields, missing_fields):
    data = extracted_fields.get("extractedFields", {})
    
    # 1. Check for Missing Mandatory Data
    if missing_fields:
        return "Manual Review", f"Mandatory fields missing: {', '.join(missing_fields)}"
    
    # 2. Identify Injury Claims (Michael Johnson's case)
    claim_type = str(data.get("claim_type", "")).lower()
    if "injury" in claim_type:
        return "Specialist Queue", "Claim involves bodily injury requiring expert handling."
    
    # 3. Handle Damage Thresholds
    try:
        damage = float(data.get("estimated_damage", 0))
        if 0 < damage < 25000:
            return "Fast-track", "Estimated damage below 25000."
    except (ValueError, TypeError):
        pass

    return "Manual Review", "Claim requires standard processing."