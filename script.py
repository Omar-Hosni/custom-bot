import os
import json
from openai.embeddings_utils import get_embedding
import openai

from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_TOKEN")

# File to store conversation history
CONVERSATION_FILE = "conversation.json"
EMBEDDING_MODEL = "text-embedding-3-small"  # Define the embedding model, better accurracy: text-embedding-ada-002

def add_embeddings_to_conversation():
    try:
        # Load existing conversation history
        if os.path.exists(CONVERSATION_FILE):
            with open(CONVERSATION_FILE, "r", encoding="utf-8") as file:
                conversation = json.load(file)
        else:
            print("Conversation file not found.")
            return

        # Add embeddings to entries without them
        for entry in conversation:
            # Get embedding for the content
            if entry["role"] == "user":
                entry["embedding"] = get_embedding(entry["content"], engine=EMBEDDING_MODEL)
                print(f"Added embedding for: {entry['content']}")

        # Save updated conversation history if changes were made
        with open(CONVERSATION_FILE, "w", encoding="utf-8") as file:
            json.dump(conversation, file, indent=4, ensure_ascii=False)
            print("Conversation updated with embeddings.")

    except Exception as e:
        print(f"Error while adding embeddings: {e}")

# print
def print_the_conv():
    with open(CONVERSATION_FILE, "r", encoding="utf-8") as file:
        conversation = json.load(file)
    for entry in conversation:
        print(entry["content"])


# delete entry with certain question / response
def delete_entry_with_content(content_to_delete):
    try:
        # Load the conversation history
        with open(CONVERSATION_FILE, "r", encoding="utf-8") as file:
            conversation_history = json.load(file)

        # Filter out entries with the specified content
        updated_conversation = [
            entry for entry in conversation_history if entry["content"] != content_to_delete
        ]

        # Save the updated conversation history back to the file
        with open(CONVERSATION_FILE, "w", encoding="utf-8") as file:
            json.dump(updated_conversation, file, indent=4, ensure_ascii=False)

        print(f"Entry with content '{content_to_delete}' deleted successfully.")

    except FileNotFoundError:
        print(f"Error: {CONVERSATION_FILE} not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON in {CONVERSATION_FILE}.")
    except Exception as e:
        print(f"Unexpected error: {e}")