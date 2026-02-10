from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from app.database.sqllite_db import get_db
from app.service.rag_service import chat_with_rag,chat_with_rag_stream
from app.service.chat_history_service import save_chat

chat_ws_router = APIRouter(prefix="/chat", tags=["Chat"])

@chat_ws_router.websocket("/ws")
async def chat_ws(websocket: WebSocket):
    await websocket.accept()
    db = next(get_db())
    try:
        while True:
            question = await websocket.receive_text()
            final_answer = ""

            for token in chat_with_rag_stream(db, question):
                if not isinstance(token, str):
                    continue

                final_answer += token
                await websocket.send_text(token)

            save_chat(db, question, final_answer)

    except WebSocketDisconnect:
        print("Client disconnected")

    finally:
        db.close()


