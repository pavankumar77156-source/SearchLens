
import re

STOP_WORDS = {
    "the", "is", "are", "a", "an",
    "and", "or", "in", "on", "for",
    "to", "of", "with", "how", "what"
}

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_keywords(text):
    cleaned_text = clean_text(text)

    words = cleaned_text.split()

    keywords = [
        word for word in words
        if word not in STOP_WORDS
    ]

    return keywords
