from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.routes.chatbot_route import chat_ws_router
from app.routes.document_upload_route import router as document_router
from app.database.sqllite_db import engine, Base

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RAG Chatbot",
    version="1.0.0"
)

# CORS (safe for local dev & frontend JS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files (JS, CSS)
app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

# Templates (Jinja2)
templates = Jinja2Templates(directory="app/templates")

# Home page
@app.get("/", tags=["UI"])
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

# API routes
app.include_router(chat_ws_router)
app.include_router(document_router)
