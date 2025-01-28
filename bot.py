import asyncio
import os
import json
import random
from typing import Final
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
from util import is_travel_related, is_greeting, greetings

# Step 0: Load token
load_dotenv()
TOKEN: Final[str] = os.getenv('BOT_TOKEN')

# File to store conversation history
CONVERSATION_FILE: Final[str] = "conversation.json"

# Main User
NOTIFY_USER_ID = 618745324030263316

# Step 1: Bot setup
intents: Intents = Intents.default()
intents.message_content = True 
client: Client = Client(intents=intents)

# Load existing conversation history
if os.path.exists(CONVERSATION_FILE):
    with open(CONVERSATION_FILE, "r", encoding="utf-8") as file:
        conversation_history = json.load(file)
else:
    print('conv.json not found')

# Step 2: Save conversation history
def save_conversation():
    with open(CONVERSATION_FILE, "w", encoding="utf-8") as file:
        json.dump(conversation_history, file, indent=4)

# Step 3: Message functionality
async def send_message(message: Message, user_message: str) -> None:

    if not user_message:
        print('(Message was empty because intents were not enabled probably)')
        return


    if is_private := user_message[0] == '?':  # Check if the message is private
        user_message = user_message[1:]
    
    try:

        if is_travel_related(user_message):
            notify_user = await client.fetch_user(NOTIFY_USER_ID)
            await notify_user.send(f"Someone asked you personal question: '{user_message}' by {message.author}")
            await message.channel.send("ill have to think about how best to answer that, ill follow up with you later ;)")
            return
        
        if is_greeting(user_message):
            await message.channel.send(random.choice(greetings))
            return

        # Get Nick's response and save history if the chat is new and unique
        response: str = get_response(user_message)

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
        if username == "meero0445":
            conversation_history.append({"role": "assistant", "content": f"{user_message}"})
        else:
            conversation_history.append({"role": "user", "content": f"{user_message}"})
        save_conversation()

# Step 6: Main event entry
def main() -> None:
    client.run(TOKEN)

if __name__ == '__main__':
    main()
