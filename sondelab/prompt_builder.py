def build_prompt(question: str, context: str) -> str:
    if not context:
        return question
    return f"Context:\n{context}\n\nQuestion:\n{question}"
