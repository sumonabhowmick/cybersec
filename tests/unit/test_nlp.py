from src.nlp.entity_extractor import extract_entities

def test_ioc_extraction():
    entities=extract_entities("Alert from 8.8.8.8 at https://evil.example/a, hash aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa CVE-2025-12345 technique T1059.001")
    assert "8.8.8.8" in entities["ips"]
    assert "evil.example" in entities["domains"]
    assert "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" in entities["hashes"]
    assert "CVE-2025-12345" in entities["cves"]
    assert "T1059.001" in entities["mitre_techniques"]
