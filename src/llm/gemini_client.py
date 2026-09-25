"""Replaceable Gemini provider using the Google GenAI SDK."""
from __future__ import annotations
import logging
from src.config.settings import GEMINI_API_KEY, GEMINI_MODEL, GEMINI_FALLBACK_MODEL
from src.llm.prompts import SYSTEM_INSTRUCTIONS, RESPONSE_SCHEMA, build_prompt
from src.llm.safety import parse_json_response

class GeminiProvider:
    def __init__(self, api_key=GEMINI_API_KEY, model=GEMINI_MODEL, fallback_model=GEMINI_FALLBACK_MODEL): self.api_key=api_key; self.model=model; self.fallback_model=fallback_model
    def analyze(self, incident: dict, prediction: dict, entities: dict, similar: list) -> dict:
        if not self.api_key: raise RuntimeError("Gemini is not configured; set GEMINI_API_KEY in .env")
        try: from google import genai
        except ImportError as exc: raise RuntimeError("Google GenAI SDK is missing; install requirements.txt") from exc
        client=genai.Client(api_key=self.api_key)
        contents=build_prompt(incident,prediction,entities,similar)
        config={"system_instruction":SYSTEM_INSTRUCTIONS,"response_mime_type":"application/json","response_json_schema":RESPONSE_SCHEMA}
        try:
            response=client.models.generate_content(model=self.model,contents=contents,config=config)
        except Exception as exc:
            status=getattr(exc,"code",getattr(exc,"status_code",None))
            if status not in {429,500,502,503,504} or self.fallback_model==self.model: raise
            logging.warning("Gemini model temporarily unavailable; retrying with configured fallback model")
            response=client.models.generate_content(model=self.fallback_model,contents=contents,config=config)
        return parse_json_response(response.text or "")

LLMService = GeminiProvider
