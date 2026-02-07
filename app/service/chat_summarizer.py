from sqlalchemy.orm import Session
from app.models.chat_history import ChatHistory
from app.models.chat_summary import ChatSummary
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_chats(db: Session, chats: list[ChatHistory]) -> ChatSummary:
    text = ""
    for chat in chats:
        text += f"User: {chat.question}\nAssistant: {chat.answer}\n"

    prompt = f"""
Summarize the following conversation concisely.
Focus on:
- User goals
- Key facts
- Decisions made
- Important context

Conversation:
{text}
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        temperature=0.2
    )

    summary_text = response.output_text.strip()

    summary = ChatSummary(
        summary=summary_text,
        start_chat_id=chats[0].id,
        end_chat_id=chats[-1].id
    )

    db.add(summary)
    db.commit()
    db.refresh(summary)

    return summary
