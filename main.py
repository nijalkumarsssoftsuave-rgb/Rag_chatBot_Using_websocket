from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import socketio

from app.routes.document_upload_route import router as document_router
from app.database.sqllite_db import engine, Base
from app.sockets.socket_file import sio

Base.metadata.create_all(bind=engine)

fastapi_app = FastAPI(title="RAG Chatbot")

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fastapi_app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

@fastapi_app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

fastapi_app.include_router(document_router)

# ✅ Critical Line
app = socketio.ASGIApp(
    sio,
    other_asgi_app=fastapi_app,
    socketio_path="socket.io"
)
