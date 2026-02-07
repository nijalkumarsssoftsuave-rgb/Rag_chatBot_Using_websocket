from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, Text
from app.database.sqllite_db import Base

class ChatSummary(Base):
    __tablename__ = "chat_summary"

    id = Column(Integer, primary_key=True)
    summary = Column(Text, nullable=False)
    start_chat_id = Column(Integer)
    end_chat_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
