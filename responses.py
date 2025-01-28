import os
import json
from gpt import generate_nick_response
from util import  find_cos_similarity, find_most_similar_entry, generate_embedding, EMBEDDING_MODEL

# File to store conversation history
CONVERSATION_FILE = "conversation.json"

# Load conversation history once at startup
try:
    with open(CONVERSATION_FILE, "r", encoding="utf-8") as file:
        conversation_history = json.load(file)
except FileNotFoundError:
    conversation_history = []

# Save conversation history to file, checking for duplicates
def save_conversation_history():
    global conversation_history

    # # Ensure there are enough messages to check
    # if len(conversation_history) < 2:
    #     return

    # # Extract the last two messages
    # new_user_msg = conversation_history[-2]
    # new_assistant_msg = conversation_history[-1]

    # # Existing history excludes the last two messages
    # existing_history = conversation_history[:-2]

    # # Check if user message is a duplicate
    # user_msg_exists = any(
    #     has_majority_common_words(entry["content"], new_user_msg["content"])
    #     for entry in existing_history
    #     if entry["role"] == "user"
    # )

    # # Check if assistant message is a duplicate
    # assistant_msg_exists = any(
    #     has_majority_common_words(entry["content"], new_assistant_msg["content"])
    #     for entry in existing_history
    #     if entry["role"] == "assistant"
    # )

    # if not (user_msg_exists or assistant_msg_exists):
        # Save the updated history to the file
    with open(CONVERSATION_FILE, "w", encoding="utf-8") as file:
        json.dump(conversation_history, file, indent=4, ensure_ascii=False)
    print("Conversation history updated successfully.")
    # else:
        # print("No changes saved; duplicates detected.")


# generate response
def get_response(user_input: str) -> str:
    global conversation_history

    # Add user message to history
    user_input_emb = generate_embedding(user_input, EMBEDDING_MODEL)
    conversation_history.append({"role": "user", 
                                 "content": user_input.lower().strip(),
                                 "embedding": user_input_emb})

    # Generate response by finding cosine similarity of other questions
    similar_response = find_most_similar_entry(query_embedding=user_input_emb,
                                               conversation=conversation_history)
    
    if similar_response:
        return similar_response #if you found similar question just return its response, and don't update the conv json
    else:
        # Generate response by gpt using current conversation history because you met a new question, not similar to prev ones
        response = generate_nick_response(conversation_history)

        # Add assistant response to history
        conversation_history.append({"role": "assistant",
                                    "content": response.lower().strip()})

        # Save updated history (checks for duplicates internally)
        save_conversation_history()

        return response
