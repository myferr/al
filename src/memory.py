import os
import json
import hashlib
from datetime import datetime
from typing import List, Dict, Optional
import pymongo
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from settings import (
    MEMORY_FILE, MONGODB_URI, MONGODB_DATABASE, MONGODB_COLLECTION,
    EMBEDDING_MODEL, MAX_CONTEXT_MESSAGES, SIMILARITY_THRESHOLD
)

class RAGMemorySystem:
    def __init__(self):
        self.client = pymongo.MongoClient(MONGODB_URI)
        self.db = self.client[MONGODB_DATABASE]
        self.collection = self.db[MONGODB_COLLECTION]
        self.encoder = SentenceTransformer(EMBEDDING_MODEL)
        
        # Create indexes for efficient querying
        self.collection.create_index([("user_hash", 1), ("timestamp", -1)])
        self.collection.create_index([("user_hash", 1), ("role", 1)])
        
    def _scramble_user_id(self, user_id: str) -> str:
        return hashlib.sha256(user_id.encode()).hexdigest()
    
    def _generate_embedding(self, text: str) -> List[float]:
        return self.encoder.encode(text).tolist()
    
    def save_message(self, user_id: str, role: str, content: str, display_name: str) -> None:
        user_hash = self._scramble_user_id(user_id)
        embedding = self._generate_embedding(content)
        
        document = {
            "user_hash": user_hash,
            "role": role,
            "content": content,
            "display_name": display_name,
            "timestamp": datetime.utcnow(),
            "embedding": embedding
        }
        
        self.collection.insert_one(document)
    
    def get_relevant_context(self, user_id: str, query: str) -> List[Dict]:
        user_hash = self._scramble_user_id(user_id)
        query_embedding = self._generate_embedding(query)
        
        # Get recent messages for this user
        recent_messages = list(self.collection.find(
            {"user_hash": user_hash},
            {"_id": 0, "content": 1, "role": 1, "embedding": 1, "timestamp": 1}
        ).sort("timestamp", -1).limit(100))  # Get last 100 messages to search through
        
        if not recent_messages:
            return []
        
        # Calculate similarities
        similarities = []
        for msg in recent_messages:
            if "embedding" in msg:
                similarity = cosine_similarity(
                    [query_embedding], 
                    [msg["embedding"]]
                )[0][0]
                similarities.append((msg, similarity))
        
        # Sort by similarity and filter by threshold
        similarities.sort(key=lambda x: x[1], reverse=True)
        relevant_messages = [
            {"role": msg["role"], "content": msg["content"]}
            for msg, sim in similarities[:MAX_CONTEXT_MESSAGES]
            if sim >= SIMILARITY_THRESHOLD
        ]
        
        # If no similar messages found, get the most recent ones
        if not relevant_messages:
            relevant_messages = [
                {"role": msg["role"], "content": msg["content"]}
                for msg in recent_messages[:MAX_CONTEXT_MESSAGES]
            ]
        
        return relevant_messages
    
    def migrate_from_jsonl(self) -> None:
        """Migrate existing JSONL memory file to MongoDB with embeddings"""
        if not os.path.exists(MEMORY_FILE):
            print("No legacy memory file found to migrate")
            return
            
        print("Migrating legacy memory file to MongoDB...")
        migrated_count = 0
        
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if all(key in entry for key in ["user_hash", "role", "content", "display_name"]):
                        # Check if already migrated
                        existing = self.collection.find_one({
                            "user_hash": entry["user_hash"],
                            "content": entry["content"],
                            "role": entry["role"]
                        })
                        
                        if not existing:
                            embedding = self._generate_embedding(entry["content"])
                            document = {
                                "user_hash": entry["user_hash"],
                                "role": entry["role"],
                                "content": entry["content"],
                                "display_name": entry["display_name"],
                                "timestamp": datetime.utcnow(),
                                "embedding": embedding,
                                "migrated": True
                            }
                            self.collection.insert_one(document)
                            migrated_count += 1
                            
                except json.JSONDecodeError as e:
                    print(f"Invalid JSON in legacy file: {line.strip()}: {e}")
                except Exception as e:
                    print(f"Error migrating entry: {e}")
        
        print(f"Migration complete: {migrated_count} entries migrated")

# Global instance
rag_memory = RAGMemorySystem()

# Legacy functions for backward compatibility
def scramble_user_id(user_id: str) -> str:
    return rag_memory._scramble_user_id(user_id)

def load_memory(user_id: str, query: Optional[str] = None):
    """Load relevant conversation history using RAG"""
    if query:
        return rag_memory.get_relevant_context(user_id, query)
    else:
        # Fallback: get recent messages if no query provided
        user_hash = rag_memory._scramble_user_id(user_id)
        recent_messages = list(rag_memory.collection.find(
            {"user_hash": user_hash},
            {"_id": 0, "content": 1, "role": 1}
        ).sort("timestamp", -1).limit(MAX_CONTEXT_MESSAGES))
        
        return [{"role": msg["role"], "content": msg["content"]} for msg in reversed(recent_messages)]

def save_message(user_id: str, role: str, content: str, display_name: str):
    """Save message with embedding generation"""
    rag_memory.save_message(user_id, role, content, display_name)

# Initialize migration on import
try:
    rag_memory.migrate_from_jsonl()
except Exception as e:
    print(f"Warning: Could not complete migration: {e}")