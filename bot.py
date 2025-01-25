import asyncio
import os
import json
from typing import Final
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

# Step 0: Load token
load_dotenv()
TOKEN: Final[str] = os.getenv('BOT_TOKEN')

# File to store conversation history
CONVERSATION_FILE: Final[str] = "conversation.json"

# Step 1: Bot setup
intents: Intents = Intents.default()
intents.message_content = True 
client: Client = Client(intents=intents)

# Load existing conversation history
if os.path.exists(CONVERSATION_FILE):
    with open(CONVERSATION_FILE, "r") as file:
        conversation_history = json.load(file)
else:
    # Initialize with a default system message
    conversation_history = [
        {"role": "system", "content": "You are Nick, a business advisor specializing in B2B strategies. Only use the information provided in the conversation history to answer questions."}
    ]

# Step 2: Save conversation history
def save_conversation():
    with open(CONVERSATION_FILE, "w") as file:
        json.dump(conversation_history, file, indent=4)

# Step 3: Message functionality
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled probably)')
        return

    if is_private := user_message[0] == '?':  # Check if the message is private
        user_message = user_message[1:]
    
    try:
        # Append user's message to the conversation history
        conversation_history.append({"role": "user", "content": user_message})

        # Get Nick's response
        response: str = get_response(user_message)

        # Append Nick's response to the conversation history
        conversation_history.append({"role": "assistant", "content": response})

        # Save the conversation to the file
        save_conversation()

        # Send response
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

# Step 4: Handling startup
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running')

# Step 5: Handling incoming messages
@client.event
async def on_message(message: Message) -> None:
    # If the message sender is the bot itself
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)
    print(f'[{channel} {username} {user_message}]')

    if channel == "general":
        await send_message(message, user_message)
    else:
        # Archive conversation for non-general channels
        conversation_history.append({"role": "user", "content": f"{username}: {user_message}"})
        save_conversation()

# Step 6: Main event entry
def main() -> None:
    client.run(TOKEN)

if __name__ == '__main__':
    main()
