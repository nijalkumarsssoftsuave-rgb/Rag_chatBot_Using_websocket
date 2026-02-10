# import socketio
# from app.database.sqllite_db import get_db
# from app.service.rag_service import chat_with_rag_stream
# from app.service.chat_history_service import save_chat

# sio = socketio.AsyncServer(
#     async_mode="asgi",
#     cors_allowed_origins="*"
# )
#
# socketio_app = socketio.ASGIApp(sio)

#
# @sio.event
# async def connect(sid, environ):
#     print(f"Socket.IO connected: {sid}")
#
#
# @sio.event
# async def disconnect(sid):
#     print(f"Socket.IO disconnected: {sid}")
#
#
# @sio.event
# async def chat_message(sid, data):
#     question = data.get("question")
#     if not question:
#         return
#
#     db = next(get_db())
#     final_answer = ""
#
#     try:
#         for token in chat_with_rag_stream(db, question):
#             if isinstance(token, str):
#                 final_answer += token
#                 await sio.emit("chat_token", token, to=sid)
#
#         save_chat(db, question, final_answer)
#         await sio.emit("chat_complete", {"status": "done"}, to=sid)
#
#     finally:
#         db.close()
