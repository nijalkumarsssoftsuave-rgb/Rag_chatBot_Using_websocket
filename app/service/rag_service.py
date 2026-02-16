from app.service.query_rewriter import rewrite_query
from app.database.chroma_db import retrieve_context
from app.service.chat_history_service import get_chat_history
from app.service.memory_manager import get_context_for_llm
from app.service.generate_answer import generate_answer
from app.service.reranker_service import rerank_chunks

def chat_with_rag(
    db,
    question: str
):
    history = get_chat_history(db, limit=6)

    chat_history = [
        {"question": c.question, "answer": c.answer}
        for c in reversed(history)
    ]

    rewritten_query = rewrite_query(question, chat_history)

    raw_chunks = retrieve_context(rewritten_query, top_k=20)

    reranked_chunks = (
        rerank_chunks(rewritten_query, raw_chunks, top_n=5)
        if raw_chunks else []
    )

    context = "\n\n".join(reranked_chunks)

    summaries, recent_chats = get_context_for_llm(db)

    answer = generate_answer(
        question=question,
        summaries=summaries,
        recent_chats=recent_chats,
        context=context,
        stream=False,   # 🔒 explicitly non-stream
    )

    return answer, context

def chat_with_rag_stream(db, question: str):
    history = get_chat_history(db, limit=6)

    chat_history = [
        {"question": c.question, "answer": c.answer}
        for c in reversed(history)
    ]

    rewritten_query = rewrite_query(question, chat_history)
    raw_chunks = retrieve_context(rewritten_query, top_k=20)

    reranked_chunks = (rerank_chunks(rewritten_query, raw_chunks, top_n=5) if raw_chunks else [])

    context = "\n\n".join(reranked_chunks)
    summaries, recent_chats = get_context_for_llm(db)

    token_generator = generate_answer(
        question=question,
        summaries=summaries,
        recent_chats=recent_chats,
        context=context,
        stream=True,
    )

    for token in token_generator:
        yield token  # already string

