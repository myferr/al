import os
import json
from settings import MEMORY_FILE

def load_memory():
    messages = []
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    messages.append(json.loads(line))
                except json.JSONDecodeError:
                    print(f"Invalid JSON: {line.strip()}")
    return messages

def save_message(role, content):
    entry = {"role": role, "content": content}
    with open(MEMORY_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry) + '\n')
