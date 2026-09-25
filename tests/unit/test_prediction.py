from src.models.predict import predict_one

class DummyPipeline:
    classes_=["Phishing","Malware"]
    def predict(self, frame):
        assert "incident_text" in frame and "failed_login_attempts" in frame
        return ["Phishing"]
    def predict_proba(self, frame): return [[.8,.2]]

def test_prediction_confidence_and_probabilities():
    result=predict_one(DummyPipeline(),{"incident_text":"credential lure"})
    assert result["label"]=="Phishing"
    assert result["confidence"]==.8
    assert result["probabilities"]["Malware"]==.2
