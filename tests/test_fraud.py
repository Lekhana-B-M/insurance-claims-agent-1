from agents.fraud_detector import check_for_fraud

def test_fraud_keywords():
    is_fraud, _ = check_for_fraud("This accident seems staged and fake.")
    assert is_fraud is True