# from app.service.query_rewriter import rewrite_query
# from app.database.chroma_db import retrieve_context
# from app.service.chat_history_service import get_chat_history
# from app.service.memory_manager import get_context_for_llm
# from app.service.generate_answer import generate_answer
# from app.service.reranker_service import rerank_chunks
#
# def chat_with_rag(
#     db,
#     question: str
# ):
#     # 🔹 1. Raw chat history (ONLY for query rewriting)
#     history = get_chat_history(db, limit=6)
#
#     chat_history = [
#         {"question": c.question, "answer": c.answer}
#         for c in reversed(history)
#     ]
#
#     rewritten_query = rewrite_query(question, chat_history)
#
#     raw_chunks = retrieve_context(rewritten_query, top_k=20)
#
#     print(f"\n\n + {raw_chunks}")
#
#     if raw_chunks:
#         reranked_chunks = rerank_chunks(rewritten_query, raw_chunks, top_n=5)
#     else:
#         reranked_chunks = []
#
#     context = "\n\n".join(reranked_chunks)
#
#     summaries, recent_chats = get_context_for_llm(db)
#
#     answer = generate_answer(
#         question=question,
#         summaries=summaries,
#         recent_chats=recent_chats,
#         context=context,
#     )
#
#     return answer, context

from app.service.query_rewriter import rewrite_query
from app.database.chroma_db import retrieve_context
from app.service.chat_history_service import get_chat_history
from app.service.memory_manager import get_context_for_llm
from app.service.reranker_service import rerank_chunks
from app.service.generate_answer import generate_answer

async def chat_with_rag_stream(
    db,
    question: str
):
    # 🔹 1. Raw chat history (for query rewriting)
    history = get_chat_history(db, limit=6)

    chat_history = [
        {"question": c.question, "answer": c.answer}
        for c in reversed(history)
    ]

    # 🔹 2. Rewrite query
    rewritten_query = rewrite_query(question, chat_history)

    # 🔹 3. Retrieve context
    raw_chunks = retrieve_context(rewritten_query, top_k=20)

    if raw_chunks:
        reranked_chunks = rerank_chunks(rewritten_query, raw_chunks, top_n=5)
    else:
        reranked_chunks = []

    context = "\n\n".join(reranked_chunks)

    # 🔹 4. Memory (summaries + recent chats)
    summaries, recent_chats = get_context_for_llm(db)

    # 🔹 5. Stream LLM response
    async for token in stream_answer(
        question=question,
        summaries=summaries,
        recent_chats=recent_chats,
        context=context
    ):
        yield token
