import openai
import os
from dotenv import load_dotenv

load_dotenv()
# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_TOKEN")


def generate_nick_response(conversation, model="gpt-4", max_tokens=200):
    """
    Generate a Nick-like response by constraining GPT to the provided conversation history.

    Args:
        conversation (list): List of conversation messages (user queries and assistant responses).
        model (str): GPT model to use.
        max_tokens (int): Maximum number of tokens in the response.

    Returns:
        str: The generated response.
    """
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=conversation,
            max_tokens=max_tokens,
            temperature=0.7,  # Strictly deterministic
            top_p=1,       # Do not limit the probability distribution
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {e}"
