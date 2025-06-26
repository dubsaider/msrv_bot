import re

PASHA_MENTION_PATTERNS = [
    re.compile(r'\bпаш(а|ей|у|е|и|енька|ка)?\b', re.IGNORECASE),
    re.compile(r'\bpasha\b', re.IGNORECASE),
]

PASHA_MENTION_THRESHOLD = 5

PASHA_THANKS_MESSAGE = "#СпасибоПаша"
