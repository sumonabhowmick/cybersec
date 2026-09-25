import pandas as pd
import pytest
from src.data.validation import validate_frame

def test_quality_report_detects_duplicate_ids_and_bad_timestamp():
    frame=pd.DataFrame({"incident_id":["x","x"],"timestamp":["2026-01-01","bad"],"incident_text":["a","b"],"threat_category":["A","A"],"severity_level":["Low","Low"]})
    result=validate_frame(frame)
    assert result["rows"]==2
    assert result["duplicate_incident_ids"]==1
    assert result["invalid_timestamps"]==1

def test_validation_requires_classification_targets():
    with pytest.raises(ValueError,match="missing required columns"):
        validate_frame(pd.DataFrame({"incident_id":["x"]}))
