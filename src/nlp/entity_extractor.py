"""Deterministic IOC extraction with optional spaCy entities."""
from __future__ import annotations
import ipaddress, re
from urllib.parse import urlparse
from src.nlp.preprocessing import normalize_text

PATTERNS = {
    "urls": re.compile(r"\bhttps?://[^\s<>\"']+", re.I),
    "emails": re.compile(r"\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b", re.I),
    "hashes": re.compile(r"\b(?:[a-f0-9]{32}|[a-f0-9]{40}|[a-f0-9]{64})\b", re.I),
    "cves": re.compile(r"\bCVE-\d{4}-\d{4,}\b", re.I),
    "mitre_techniques": re.compile(r"\bT\d{4}(?:\.\d{3})?\b", re.I),
    "ports": re.compile(r"\b(?:port\s*[:=]?\s*)(\d{1,5})\b", re.I),
    "usernames": re.compile(r"\b(?:user(?:name)?|account)\s*[:=]\s*([\w.$-]{2,64})", re.I),
    "file_names": re.compile(r"\b[\w.-]+\.(?:exe|dll|ps1|bat|cmd|js|vbs|docm|xlsm|pdf|zip)\b", re.I),
}

def extract_entities(value: object, include_spacy: bool = False) -> dict[str, list[str]]:
    text = normalize_text(value)
    out = {k: sorted(set(m.group(1) if k in {"ports", "usernames"} else m.group(0) for m in p.finditer(text)), key=str.lower) for k,p in PATTERNS.items()}
    ips = []
    for candidate in re.findall(r"(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])", text):
        try: ips.append(str(ipaddress.ip_address(candidate)))
        except ValueError: pass
    try:
        import ipaddress as _ip
        for candidate in re.findall(r"(?<![\w:])(?:[0-9a-f]{0,4}:){2,7}[0-9a-f]{0,4}(?![\w:])", text, re.I):
            try: ips.append(str(_ip.ip_address(candidate)))
            except ValueError: pass
    except ImportError: pass
    domains = set(re.findall(r"\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}\b", text, re.I))
    for url in out["urls"]:
        host = urlparse(url).hostname
        if host: domains.add(host.lower())
    out["ips"] = sorted(set(ips)); out["domains"] = sorted(domains)
    out["ports"] = sorted({p for p in out["ports"] if p.isdigit() and int(p) <= 65535}, key=int)
    out["usernames"] = sorted(set(out["usernames"] + re.findall(r"\b(?:analyst|employee|admin|user)\w{1,32}\b", text, re.I)), key=str.lower)
    out["suspicious_keywords"] = sorted(set(re.findall(r"\b(?:ransomware|exfiltration|phishing|beaconing|privilege escalation|command and control|credential theft|malware|powershell|lateral movement)\b", text, re.I)), key=str.lower)
    if include_spacy:
        try:
            import spacy
            nlp = spacy.load("en_core_web_sm")
            out["named_entities"] = sorted({e.text for e in nlp(text).ents if e.label_ in {"PERSON", "ORG", "GPE", "PRODUCT"}})
        except (ImportError, OSError): out["named_entities"] = []
    return out
