import openai
import os
from dotenv import load_dotenv
import random
load_dotenv()
# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_TOKEN")


def generate_nick_response(conversation, model="gpt-4-1106-preview", max_tokens=150):

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=conversation,
            max_tokens=max_tokens,
            temperature=random.choice([0, 0.1, 0.2, 0.3, 0.4]),  # Slight creativity while staying focused
            top_p=0.95,        # Balanced diversity for natural responses
            presence_penalty=0.2,  # Discourage repetition of ideas
            frequency_penalty=0.1  # Avoid repeated words
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {e}"
