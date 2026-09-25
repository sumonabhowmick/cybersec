"""Compatibility entry point for IOC extraction."""
from src.nlp.entity_extractor import extract_entities

def extract_iocs(text: object) -> dict[str, list[str]]:
    return extract_entities(text)
