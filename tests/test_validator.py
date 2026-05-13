#import pytest
from agents.field_validator import validate_fields

def test_missing_fields():
    sample = {"extractedFields": {"policy_number": "123"}}
    missing = validate_fields(sample)
    assert "policyholder_name" in missing
    assert "policy_number" not in missing