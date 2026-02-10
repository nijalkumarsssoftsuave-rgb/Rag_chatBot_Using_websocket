# import socketio
# from app.database.sqllite_db import get_db
# from app.service.rag_service import chat_with_rag_stream
# from app.service.chat_history_service import save_chat
#
# sio = socketio.AsyncServer(
#     async_mode="asgi",
#     cors_allowed_origins="*"
# )
#
# socket_app = socketio.ASGIApp(sio)
#
#
# @sio.event
# async def connect(sid, environ):
#     print(f"Socket.IO Client connected: {sid}")
#
#
# @sio.event
# async def disconnect(sid):
#     print(f"Socket.IO Client disconnected: {sid}")
#
#
# # Custom event instead of websocket loop
# @sio.event
# async def chat_message(sid, data):
#     """
#     data = { "question": "your question here" }
#     """
#     question = data.get("question")
#     db = next(get_db())
#     final_answer = ""
#
#     try:
#         for token in chat_with_rag_stream(db, question):
#             if not isinstance(token, str):
#                 continue
#
#             final_answer += token
#
#             # Send token back to SAME client
#             await sio.emit("chat_token", token, room=sid)
#
#         save_chat(db, question, final_answer)
#
#         # Tell client stream is done
#         await sio.emit("chat_complete", {"status": "done"}, room=sid)
#
#     finally:
#         db.close()
