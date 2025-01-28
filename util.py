import os
from gpt import generate_nick_response
import openai
from openai.embeddings_utils import get_embedding, cosine_similarity
import numpy as np
from typing import Optional
import json

greetings = [
    "hi", "hey", "hello", "yo", "sup", "what's up", "howdy", "hiya",
    "hey there", "hello there", "how's it going", "how's everything",
    "what's happening", "good day", "greetings", "salutations",
    "hi there", "how are you", "how have you been", "how do you do",
    "what's good", "what's new", "morning", "good morning", "good afternoon",
    "good evening", "evening", "hiya there", "aloha", "hola", "bonjour",
    "hallo", "ciao", "namaste", "salaam", "shalom", "konnichiwa", "annyeong"
]

EMBEDDING_MODEL = "text-embedding-3-small"
SIMILARITY_THRESHOLD = 0.85  # Tune this based on testing
openai.api_key = os.getenv("OPENAI_TOKEN")


def is_greeting(message: str) -> bool:
    return message.lower() in greetings

def generate_embedding(query, engine):
    return get_embedding(query, engine)

def find_cos_similarity(current_embedding, stored_embedding):
    return cosine_similarity(current_embedding, stored_embedding)

def is_travel_related(message: str) -> bool:

    if len(message) < 3:
        return False

    try:
        temp_conversation = [
            {"role": "system", "content": "You are a travel expert. Your job is to identify if a given question is related to travel, such as trips, locations, or travel plans. If it is unrelated, say 'no'. If it is travel-related, say 'yes'."},
            {"role": "user", "content": f"Is this message about traveling? {message}"}
        ]
        response = generate_nick_response(temp_conversation, max_tokens=50)
        return "yes" in response.lower()
    except Exception as e:
        print(f"Error in travel detection: {e}")
        return False


def has_majority_common_words(str1: str, str2: str, threshold: float = 60.0) -> bool:
    # Convert strings to sets of words
    words1 = set(str1.split())
    words2 = set(str2.split())

    # Find common words
    common_words = words1 & words2

    # Calculate the percentage of overlap (relative to the smaller set)
    smaller_set_size = min(len(words1), len(words2))
    if smaller_set_size == 0:  # Avoid division by zero
        return False

    overlap_percentage = (len(common_words) / smaller_set_size) * 100

    # Check if the overlap exceeds the threshold
    return overlap_percentage > threshold



def find_most_similar_entry(query_embedding, conversation):
    """
    Find the most similar entry in the conversation history based on cosine similarity.
    If the similarity score exceeds the threshold, return the next assistant entry.
    """
    try:

        # Calculate similarity with each entry
        similarities = []
        for i, entry in enumerate(conversation):
            if "embedding" in entry and entry["role"] == "user":  # Ensure the entry has an embedding and it is a question by a user
                similarity = cosine_similarity(query_embedding, entry["embedding"])
                similarities.append((similarity, i))

        # Find the most similar entry
        if similarities:
            most_similar = max(similarities, key=lambda x: x[0])
            similarity_score, index = most_similar

            # Check if the similarity score exceeds the threshold
            if similarity_score >= SIMILARITY_THRESHOLD:
                # Find the next "assistant" entry after the most similar user message
                for next_entry in conversation[index + 1:]:
                    if next_entry["role"] == "assistant":
                        return next_entry["content"]  # Return the assistant's response
        return None  # No match found within the threshold

    except Exception as e:
        print(f"Error finding the most similar entry: {e}")
        return None