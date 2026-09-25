import pandas as pd
from src.data.cleaning import clean_frame

def test_cleaning_removes_duplicate_ids_and_preserves_security_tokens():
    row={"incident_id":"i-1","timestamp":"2026-01-01","incident_text":" CVE-2025-1234 powershell.exe  ","threat_category":"Malware","severity_level":"High","source_port":65536,"destination_port":443}
    duplicate=dict(row,incident_text="Different text, same incident id")
    frame=pd.DataFrame([row,duplicate])
    cleaned,report=clean_frame(frame)
    assert len(cleaned)==1 and report["duplicate_incident_ids_removed"]==1
    assert "CVE-2025-1234" in cleaned.iloc[0].incident_text
    assert pd.isna(cleaned.iloc[0].source_port)
