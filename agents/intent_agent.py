# agents/intent_agent.py

import re

def extract_keywords(message: str):
    message = message.lower()

    # remove punctuation
    message = re.sub(r"[^\w\s]", " ", message)

    words = message.split()

    # remove very small words
    keywords = [w for w in words if len(w) > 2]

    return keywords