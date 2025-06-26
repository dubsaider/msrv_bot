import re

ALL_MENTION_PATTERNS = [
    ("Паша", re.compile(r'\bпаш(а|ей|у|е|и|енька|ка)?\b', re.IGNORECASE)),
    ("Pasha", re.compile(r'\bpasha\b', re.IGNORECASE)),
    
    ("ЗАхар", re.compile(r'\bзахар(а|у|ом|е|чик|ка)?\b', re.IGNORECASE)),
    ("Zakhar", re.compile(r'\bzahar\b', re.IGNORECASE)),
    
    ("Дед", re.compile(r'\bдед(а|у|ом|е|ок|ушка)?\b', re.IGNORECASE)),
    ("Ded", re.compile(r'\bded\b', re.IGNORECASE)),

    # Убедитесь, что все остальные записи также имеют ровно два элемента.
    # ("NewName", re.compile(r'\bноваявариация1\b', re.IGNORECASE)),
]

GLOBAL_MENTION_THRESHOLD = 5

def generate_thanks_message(name: str) -> str:
    return f"#Спасибо{name}"
