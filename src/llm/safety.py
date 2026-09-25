"""Bound inputs and outputs from analyst-assistance model providers."""
import json

def validate_analysis(result: dict) -> dict:
    required={"summary":str,"investigation_steps":list,"recommended_actions":list,"risk_notes":list,"model_explanation":str}
    if not isinstance(result,dict): raise ValueError("LLM response must be a JSON object")
    for key, kind in required.items():
        if key not in result or not isinstance(result[key],kind): raise ValueError(f"LLM response has invalid field: {key}")
    for key in ("investigation_steps","recommended_actions","risk_notes"):
        result[key]=[str(v)[:1000] for v in result[key][:12]]
    for key in ("summary","model_explanation"): result[key]=result[key][:4000]
    return result

def parse_json_response(text: str) -> dict:
    try: return validate_analysis(json.loads(text))
    except (json.JSONDecodeError, TypeError) as exc: raise ValueError("Gemini returned malformed JSON") from exc
