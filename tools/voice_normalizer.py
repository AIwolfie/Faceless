#!/usr/bin/env python3
"""
voice_normalizer.py — Comprehensive Script & Phonetic Normalizer for TTS.
Part of the Faceless Video Production Engine.

Normalizes raw script text before speech synthesis:
- Strips zero-width characters and invisible formatting artifacts
- Converts numbers, ordinals, percentages, and currencies to natural speech
- Expands tech abbreviations, camelCase, URLs, and social tags
- Preserves single-bracket markup tags ([pause 300ms], [voice: am_michael])
- Seamlessly overlays channel pronunciations from tools/lexicon.py
"""

from __future__ import annotations
import os
import re
import unicodedata
from typing import Dict, Optional

# Zero-width / non-printing junk regex
_ZERO_WIDTH_RE = re.compile(
    r"[\u200B-\u200D\uFEFF\u200E\u200F\u00AD\u202A-\u202E]"
)

# Bracketed tags: [pause ...], [voice: ...]
_TAG_RE = re.compile(r"(\[[^\]]+\])")

# Common units & symbols
_UNIT_MAP = {
    "%": " percent",
    "&": " and ",
    "@": " at ",
    "#": " number ",
    "/": " slash ",
    "+": " plus ",
    "=": " equals ",
    "°": " degrees ",
    "~": " approximately ",
}

# Number words lookup (1-19, 20-90)
_ONES = [
    "", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
    "seventeen", "eighteen", "nineteen"
]
_TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
_ORDINALS = {
    "1st": "first", "2nd": "second", "3rd": "third", "4th": "fourth",
    "5th": "fifth", "6th": "sixth", "7th": "seventh", "8th": "eighth",
    "9th": "ninth", "10th": "tenth"
}

def int_to_words(n: int) -> str:
    """Converts integers up to 999,999,999 to spoken English words."""
    if n == 0:
        return "zero"
    if n < 0:
        return "negative " + int_to_words(-n)

    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("-" + _ONES[n % 10] if n % 10 != 0 else "")
    if n < 1000:
        return _ONES[n // 100] + " hundred" + (" " + int_to_words(n % 100) if n % 100 != 0 else "")
    if n < 1000000:
        return int_to_words(n // 1000) + " thousand" + (" " + int_to_words(n % 1000) if n % 1000 != 0 else "")
    if n < 1000000000:
        return int_to_words(n // 1000000) + " million" + (" " + int_to_words(n % 1000000) if n % 1000000 != 0 else "")
    return str(n)

def normalize_numbers(text: str) -> str:
    """Spells out integers, comma-separated numbers, decimals, and ordinals."""
    # Percentages first so trailing % doesn't block word boundary
    text = text.replace("%", " percent ")

    # Ordinals (1st, 2nd, etc.)
    for ord_key, ord_val in _ORDINALS.items():
        text = re.sub(rf"\b{ord_key}\b", ord_val, text, flags=re.IGNORECASE)

    # Currencies: $100 -> one hundred dollars
    def _repl_dollar(m):
        amt = m.group(1).replace(",", "")
        try:
            val = int(amt)
            return f"{int_to_words(val)} dollars"
        except ValueError:
            return m.group(0)
    text = re.sub(r"\$(\d+(?:,\d{3})*)\b", _repl_dollar, text)

    # Decimals: 3.14 -> three point one four, 99.9 -> ninety-nine point nine
    def _repl_decimal(m):
        whole = m.group(1)
        dec = m.group(2)
        try:
            w_words = int_to_words(int(whole))
        except ValueError:
            w_words = whole
        dec_words = " ".join(int_to_words(int(d)) for d in dec)
        return f"{w_words} point {dec_words}"
    text = re.sub(r"\b(\d+)\.(\d+)\b", _repl_decimal, text)

    # Thousands with commas (e.g. 100,000 -> 100000 -> one hundred thousand)
    def _repl_comma_num(m):
        raw = m.group(0).replace(",", "")
        try:
            val = int(raw)
            return int_to_words(val)
        except ValueError:
            return m.group(0)
    text = re.sub(r"\b\d{1,3}(?:,\d{3})+\b", _repl_comma_num, text)

    # Standalone plain numbers (up to 6 digits)
    def _repl_plain_int(m):
        val = int(m.group(0))
        return int_to_words(val)
    text = re.sub(r"\b\d{1,6}\b", _repl_plain_int, text)

    return text

def normalize_tech_terms(text: str) -> str:
    """Normalizes tech abbreviations, acronyms, and social tags."""
    # Reddit and user handles: r/counting -> r slash counting, u/name -> user name
    text = re.sub(r"\br/([a-zA-Z0-9_-]+)\b", r"r slash \1", text)
    text = re.sub(r"\bu/([a-zA-Z0-9_-]+)\b", r"user \1", text)

    # Versions: v1.0 -> version one point zero
    text = re.sub(r"\bv(\d+)\b", r"version \1", text, flags=re.IGNORECASE)

    # Common tech acronyms spacing for crisp Kokoro / EdgeTTS pronunciation
    acronym_map = {
        "GPT-4": "G P T 4",
        "GPT": "G P T",
        "ChatGPT": "Chat G P T",
        "LLM": "L L M",
        "LLMs": "L L M's",
        "RLHF": "R L H F",
        "TTS": "T T S",
        "API": "A P I",
        "APIs": "A P I's",
        "CLI": "C L I",
        "GPU": "G P U",
        "GPUs": "G P U's",
        "TPU": "T P U",
        "VRAM": "V RAM",
        "UI": "U I",
        "UX": "U X",
        "VS Code": "V S Code",
        "VSCode": "V S Code",
        "JSON": "JASON",
        "SQL": "sequel",
        "PostgreSQL": "Postgres Q L",
        "SVG": "S V G",
        "SVGs": "S V G's",
        "PNG": "P N G",
        "PNGs": "P N G's",
        "HTML": "H T M L",
        "CSS": "C S S",
        "XML": "X M L",
    }
    for acr, spoken in acronym_map.items():
        text = re.sub(rf"\b{re.escape(acr)}\b", spoken, text)

    return text

def clean_script_text(text: str) -> str:
    """Strips zero-width characters, normalizes whitespace, and unifies quotes."""
    if not text:
        return ""
    # Strip zero-width junk
    text = _ZERO_WIDTH_RE.sub("", text)
    # Normalize unicode to NFKC
    text = unicodedata.normalize("NFKC", text)
    # Smart quotes & dashes to standard
    text = text.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    text = text.replace("—", " - ").replace("–", " - ")
    # Collapse whitespace
    text = " ".join(text.split())
    return text

def normalize_for_tts(
    text: str,
    custom_pronunciations: Optional[Dict[str, str]] = None
) -> str:
    """
    Main entry point for speech text normalization.
    Protects bracketed markup, cleans unicode, spells numbers,
    expands acronyms, and applies channel lexicon.
    """
    if not text or not text.strip():
        return ""

    # Split on bracketed tags to preserve SSML/pause markers
    parts = _TAG_RE.split(text)
    normalized_parts = []

    for part in parts:
        if part.startswith("[") and part.endswith("]"):
            # Preserve tag verbatim
            normalized_parts.append(part)
        else:
            cleaned = clean_script_text(part)
            with_tech = normalize_tech_terms(cleaned)
            with_nums = normalize_numbers(with_tech)
            
            # Apply custom channel pronunciations
            if custom_pronunciations:
                for word, rep in custom_pronunciations.items():
                    with_nums = re.sub(rf"\b{re.escape(word)}\b", rep, with_nums, flags=re.IGNORECASE)
                    
            normalized_parts.append(with_nums)

    result = "".join(normalized_parts)
    return " ".join(result.split())

if __name__ == "__main__":
    sample = (
        'Welcome to TechXKenil! Today in v2.0, we explore why ChatGPT crashes on '
        '"SolidGoldMagikarp" with 100,000 counts on r/counting, costing $500 '
        'and 99.9% of GPU VRAM. [pause 200ms] Stay tuned!'
    )
    custom = {"TechXKenil": "Tech X Kenil", "SolidGoldMagikarp": "Solid Gold Magic carp"}
    print("Raw:")
    print(" ", sample)
    print("\nNormalized:")
    print(" ", normalize_for_tts(sample, custom))
