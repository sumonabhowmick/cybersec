from src.database.queries import INSERT_FEEDBACK, INSERT_INCIDENT

def test_database_statements_parameterize_values():
    assert "%s" in INSERT_FEEDBACK
    assert "%s" in INSERT_INCIDENT
    assert "incident_id='" not in INSERT_INCIDENT
