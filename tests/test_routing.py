from agents.routing_engine import determine_route

def test_fast_track():
    data = {"extractedFields": {"estimated_damage": 5000, "claim_type": "Auto"}}
    route, _ = determine_route(data, [])
    assert route == "Fast-track"

def test_manual_review_on_missing():
    data = {"extractedFields": {"estimated_damage": 5000}}
    route, _ = determine_route(data, ["policy_number"])
    assert route == "Manual Review"