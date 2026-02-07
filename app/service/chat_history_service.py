from sqlalchemy.orm import Session
from app.models.chat_history import ChatHistory

from app.service.memory_manager import maybe_summarize

def save_chat(db, question, answer):
    chat = ChatHistory(question=question, answer=answer)
    db.add(chat)
    db.commit()
    db.refresh(chat)

    maybe_summarize(db)

    return chat

def get_chat_history(
    db: Session,
    limit: int = 10
):
    return (
        db.query(ChatHistory)
        .order_by(ChatHistory.created_at.desc())
        .limit(limit)
        .all()
    )
