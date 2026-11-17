#!/usr/bin/env python3
"""
speech_chunker.py — Natural Sentence and Semantic Clause Boundary Chunking.
Part of the Faceless Video Production Engine.

Splits script narration into natural spoken chunks, respecting:
- Abbreviations, honorifics, and acronyms ("Dr.", "Mr.", "e.g.", "i.e.", "U.S.")
- Numerical expressions, decimals, and clock times ("3.14", "10.5k", "9:30 AM")
- URLs and file paths ("github.com/techXkenil", "render.py")
- Ellipses and parentheticals ("... ", " — ")
- Bracketed audio tags and pauses ("[pause 300ms]")
"""

from __future__ import annotations
import re
from typing import List, Tuple

# Default minimum sentence length before emitting
DEFAULT_MIN_SENTENCE_LEN = 24
DEFAULT_MIN_WORDS_FOR_SHORT_FLUSH = 1

HONORIFICS = (
    "Mr", "Mrs", "Ms", "Dr", "Prof", "Gen", "Sen", "Rep", "Lt",
    "Col", "Capt", "Sgt", "St", "Gov", "Maj", "Rev", "Pres"
)

COMMON_ABBREVIATIONS = (
    "e.g", "i.e", "vs", "etc", "approx", "appx", "dept", "min", "max",
    "est", "inc", "corp", "co", "ltd", "vol", "no", "rev", "ed"
)

# Compile honorific and abbreviation guard regex
_HONORIFICS_RE = re.compile(
    r"\b(" + "|".join(HONORIFICS + COMMON_ABBREVIATIONS) + r")\.",
    re.IGNORECASE
)

# Marker substitutions for safe splitting
_DOT_MARKER = "___DOT___"
_ELLIPSIS_MARKER = "___ELLIPSIS___"
_URL_MARKER = "___URLDOT___"

def _protect_tokens(text: str) -> str:
    """Replaces periods in protected tokens (abbreviations, decimals, URLs) with markers."""
    # 1. Ellipsis
    text = re.sub(r"\.{3,}", _ELLIPSIS_MARKER, text)
    
    # 2. URLs / domains
    text = re.sub(r"([a-zA-Z0-9_-]+)\.([a-zA-Z]{2,6})\b", rf"\1{_URL_MARKER}\2", text)
    
    # 3. Decimals & numbers (e.g., 3.14, $19.99, v1.0)
    text = re.sub(r"(\d)\.(\d)", rf"\1{_DOT_MARKER}\2", text)
    
    # 4. Honorifics and abbreviations
    def _repl_abbr(m):
        return m.group(1) + _DOT_MARKER
    text = _HONORIFICS_RE.sub(_repl_abbr, text)
    
    # 5. Acronyms (e.g. U.S.A., I.D.)
    text = re.sub(r"\b([A-Za-z])\.([A-Za-z])\.", rf"\1{_DOT_MARKER}\2{_DOT_MARKER}", text)
    return text

def _unprotect_tokens(text: str) -> str:
    """Restores protected period markers."""
    text = text.replace(_ELLIPSIS_MARKER, "...")
    text = text.replace(_URL_MARKER, ".")
    text = text.replace(_DOT_MARKER, ".")
    return text

def split_sentences(text: str, min_len: int = DEFAULT_MIN_SENTENCE_LEN) -> List[str]:
    """
    Splits continuous prose or script text into clean, natural spoken sentences.
    Preserves acronyms, decimals, and bracketed SSML markers.
    """
    if not text or not text.strip():
        return []

    cleaned = " ".join(text.strip().split())
    protected = _protect_tokens(cleaned)

    # Split on sentence terminators followed by whitespace or end of string
    raw_splits = re.split(r"([.!?]+(?:\s+|$))", protected)
    
    chunks = []
    current = ""
    
    for i in range(0, len(raw_splits) - 1, 2):
        sentence_body = raw_splits[i]
        punct = raw_splits[i + 1]
        sentence = _unprotect_tokens((sentence_body + punct).strip())
        
        if not sentence:
            continue
            
        if current:
            # If current buffered chunk is too short, merge with next
            if len(current) < min_len:
                current = f"{current} {sentence}"
            else:
                chunks.append(current)
                current = sentence
        else:
            current = sentence

    # Last segment
    if len(raw_splits) % 2 == 1 and raw_splits[-1].strip():
        tail = _unprotect_tokens(raw_splits[-1].strip())
        if current:
            current = f"{current} {tail}"
        else:
            current = tail

    if current:
        chunks.append(current)

    return chunks

def chunk_for_speech_pacing(
    text: str,
    max_words_per_beat: int = 18,
    min_words_per_beat: int = 5
) -> List[str]:
    """
    Splits long narrative sentences into rhythm-balanced speech beats
    at natural semantic clause boundaries (commas, semicolons, dashes).
    """
    sentences = split_sentences(text)
    beats = []

    for s in sentences:
        words = s.split()
        if len(words) <= max_words_per_beat:
            beats.append(s)
            continue

        # Split on commas, colons, semicolons, em-dashes
        clauses = re.split(r"([,;:\u2014\-]\s+)", s)
        cur_beat = ""
        
        for i in range(0, len(clauses), 2):
            clause_text = clauses[i]
            delim = clauses[i + 1] if i + 1 < len(clauses) else ""
            part = (clause_text + delim).strip()
            
            if not part:
                continue

            test_combo = f"{cur_beat} {part}".strip() if cur_beat else part
            if len(test_combo.split()) > max_words_per_beat and cur_beat:
                beats.append(cur_beat)
                cur_beat = part
            else:
                cur_beat = test_combo

        if cur_beat:
            beats.append(cur_beat)

    return beats

if __name__ == "__main__":
    test_text = (
        "There is a secret word that makes ChatGPT glitch, crash, and insult users: "
        "SolidGoldMagikarp. It came from Reddit, where user u/SolidGoldMagikarp posted "
        "over 100,000 times on r/counting! With zero training weights in GPT-4, "
        "it became an unmapped black hole."
    )
    print("Sentences:")
    for i, s in enumerate(split_sentences(test_text), 1):
        print(f"  {i}. {s}")
    print("\nBeats:")
    for i, b in enumerate(chunk_for_speech_pacing(test_text, max_words_per_beat=12), 1):
        print(f"  [{i}] ({len(b.split())} words) {b}")
