import os
import json
import hashlib
from settings import MEMORY_FILE

def scramble_user_id(user_id: str) -> str:
    return hashlib.sha256(user_id.encode()).hexdigest()

def load_memory(user_id: str):
    user_hash = scramble_user_id(user_id)
    messages = []
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if entry.get("user_hash") == user_hash:
                        messages.append({"role": entry["role"], "content": entry["content"]})
                except json.JSONDecodeError:
                    print(f"Invalid JSON: {line.strip()}")
    return messages

def save_message(user_id: str, role: str, content: str, display_name: str):
    user_hash = scramble_user_id(user_id)
    entry = {
        "user_hash": user_hash,
        "role": role,
        "content": content,
        "display_name": display_name
    }
    with open(MEMORY_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry) + '\n')
