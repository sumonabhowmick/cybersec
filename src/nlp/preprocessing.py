"""Normalize incident text while preserving security-specific tokens."""
from __future__ import annotations
import re

_SPACE = re.compile(r"\s+")
_CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")

def normalize_text(value: object) -> str:
    if value is None: return ""
    text = _CONTROL.sub(" ", str(value))
    text = _SPACE.sub(" ", text).strip()
    return text

def tokenize(value: object) -> list[str]:
    # Keep domains, hashes, IPv4, CVEs, MITRE IDs, flags, and punctuation-bearing commands.
    text = normalize_text(value).lower()
    return re.findall(r"(?:https?://\S+|[\w.+-]+@[\w.-]+|cve-\d{4}-\d+|t\d{4}(?:\.\d{3})?|(?:[0-9a-f]{32,64})|(?:\d{1,3}\.){3}\d{1,3}|[\w.-]+|--?[\w-]+)", text, flags=re.I)

def split_sentences(value: object) -> list[str]:
    """Use NLTK when its tokenizer data is installed; retain an offline fallback."""
    text=normalize_text(value)
    if not text: return []
    try:
        from nltk.tokenize import sent_tokenize
        return sent_tokenize(text)
    except (ImportError,LookupError):
        return [part.strip() for part in re.split(r"(?<=[.!?])\s+",text) if part.strip()]
