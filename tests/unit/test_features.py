from src.features.feature_schema import schema

def test_targets_and_postincident_data_are_excluded_from_features():
    policy=schema()
    assert "threat_category" not in policy["available_at_ingestion"]
    assert "severity_level" not in policy["available_at_ingestion"]
    assert "investigation_notes" in policy["post_incident_excluded"]
    assert "priority" in policy["leakage_prone_excluded"]
