from sqlalchemy.orm import Session
from app.models.chat_history import ChatHistory
from app.models.chat_summary import ChatSummary
from app.service.chat_summarizer import summarize_chats

SUMMARY_BATCH_SIZE = 6

def get_context_for_llm(db: Session):
    # 🔹 Fetch ALL summaries (long-term memory)
    summaries = (
        db.query(ChatSummary)
        .order_by(ChatSummary.start_chat_id.asc())
        .all()
    )

    # 🔹 Fetch recent raw chats (working memory)
    recent_chats = (
        db.query(ChatHistory)
        .order_by(ChatHistory.id.desc())
        .limit(4)
        .all()
    )

    recent_chats.reverse()

    return summaries, recent_chats

def maybe_summarize(db: Session):
    total_chats = db.query(ChatHistory).count()

    if total_chats % 6 != 0:
        return

    chats = (
        db.query(ChatHistory)
        .order_by(ChatHistory.id.desc())
        .limit(6)
        .all()
    )

    chats.reverse()
    summarize_chats(db, chats)
