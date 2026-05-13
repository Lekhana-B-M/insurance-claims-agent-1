import logging

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def validate_fields(extracted_data):
    from config.fields_config import MANDATORY_FIELDS
    
    data = extracted_data.get("extractedFields", {})
    missing_fields = []
    
    for field in MANDATORY_FIELDS:
        value = data.get(field)
        if value is None or str(value).strip() == "" or str(value).lower() == "null":
            missing_fields.append(field)
            
    return missing_fields

# --- Independent Test ---
if __name__ == "__main__":
    # Dummy data to test the logic
    sample_data = {
        "extractedFields": {
            "policy_number": "ABC-123",
            "policyholder_name": "",  # Empty
            "incident_date": "2024-01-01",
            "estimated_damage": None  # Missing
        }
    }
    missing = validate_fields(sample_data)
    print(f"\nFinal Missing Fields List: {missing}")