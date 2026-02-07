from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def rewrite_query(user_input: str, chat_history: list[dict]) -> str:
    """
    Converts short replies like 'yes', 'tell me more'
    into a full standalone question.
    """

    history_text = ""
    for turn in chat_history[-4:]:
        history_text += f"""
User: {turn['question']}
Assistant: {turn['answer']}
"""

    prompt = f"""
You are a query rewriter for a document-based assistant.

Conversation so far:
{history_text}

User reply:
"{user_input}"

Rewrite the user reply into a complete, self-contained question
that can be used to search documents.
If the reply already looks like a full question, return it unchanged.
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        temperature=0
    )

    return response.output_text.strip()
