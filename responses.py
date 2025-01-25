import json
from gpt import generate_nick_response

# File to store conversation history
CONVERSATION_FILE = "conversation.json"

# Load conversation history from file
def load_conversation_history():
    try:
        with open(CONVERSATION_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # Initialize with a default system message if the file doesn't exist
        return [
            {"role": "system", "content": "You are Nick, a business advisor specializing in B2B strategies. Only use the information provided in the conversation history to answer questions."}
        ]

# Save updated conversation history to file
def save_conversation_history(conversation):
    with open(CONVERSATION_FILE, "w") as file:
        json.dump(conversation, file, indent=4)

def get_response(user_input) -> str:
    lowered: str = user_input.lower()

    # Load existing conversation history
    conversation = load_conversation_history()

    # Add the new user query to the conversation history
    conversation.append({"role": "user", "content": lowered})

    # Generate Nick's response
    response = generate_nick_response(conversation)

    # Add Nick's response to the conversation history
    conversation.append({"role": "assistant", "content": response})

    # Save updated conversation history
    save_conversation_history(conversation)

    return response
