from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank_chunks(
    query: str,
    chunks,
    top_n: int = 5
) -> list[str]:
    """
    chunks can be:
    - list[str]
    - list[dict]
    - list[Document]
    """

    if not chunks:
        return []

    texts = []

    for c in chunks:
        if isinstance(c, str):
            texts.append(c)
        elif isinstance(c, dict):
            texts.append(c.get("text") or c.get("page_content"))
        else:
            # Chroma / LangChain Document
            texts.append(getattr(c, "page_content", str(c)))

    texts = [t[:1000] for t in texts if t]

    pairs = [(query, text) for text in texts]

    for i, (q, t) in enumerate(pairs, start=1):
        print(f"\nPAIR {i}")
        print("QUERY:")
        print(q)
        print("TEXT:")
        print(t[:500])

    scores = reranker.predict(pairs)

    # print(f"\nSCORES:{scores}")

    ranked = sorted(
        zip(texts, scores),
        key=lambda x: x[1],
        reverse=True
    )

    # print(f"\nRANKED:{ranked}")

    return [text for text, _ in ranked[:top_n]]

