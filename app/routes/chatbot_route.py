# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from app.database.sqllite_db import get_db
# from app.service.rag_service import chat_with_rag
# from app.service.chat_history_service import save_chat
# from app.pydantics.chat_pyandics import ChatRequest
#
# chat_router = APIRouter(prefix="/chat", tags=["Chat"])
#
# @chat_router.post("/")
# def chat(
#     payload: ChatRequest,
#     db: Session = Depends(get_db)
# ):
#     question = payload.message
#     answer, context = chat_with_rag(db, question)
#
#     save_chat(db, question, answer)
#
#     return {
#         "message": answer
#     }

from fastapi import APIRouter, WebSocket, Depends
from sqlalchemy.orm import Session
from app.database.sqllite_db import get_db
from app.service.rag_service import chat_with_rag_stream
from app.service.chat_history_service import save_chat

chat_router = APIRouter(prefix="/chat", tags=["Chat"])

@chat_router.websocket("/")
async def chat_ws(
    websocket: WebSocket,
    db: Session = Depends(get_db)
):
    await websocket.accept()

    try:
        while True:
            question = await websocket.receive_text()

            full_answer = ""

            async for token in chat_with_rag_stream(db, question):
                full_answer += token
                await websocket.send_text(token)

            # 🔹 Save chat AFTER streaming completes
            save_chat(db, question, full_answer)

    except Exception:
        await websocket.close()
