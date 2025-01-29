# NickBot

NickBot is a conversational bot that simulates a business advisor named "Nick." It uses OpenAI's GPT API, and Embedding to store and generate responses and maintains a persistent conversation history in a `conversation.json` file.

## Features

- **Simulates Nick:** Nick is a B2B business advisor who provides strategic advice to users.
- **Persistent Conversations:** Tracks and saves all unique user-bot and user-consultant interactions in `conversation.json`.
- **Custom Responses:** Generates tailored responses based on the context of the conversation or from similar previous chats.

---

## Installation

### Prerequisites

- Python 3.8 or higher
- An OpenAI API key
- A Discord bot token
- Required Python packages (see below)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd NickBot
python/python3 bot.py
