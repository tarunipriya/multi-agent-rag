from core.vector_store import get_retriever
from core.llm import get_llm

def retrieve_chunks(question: str, top_k: int = 5):
    """
    Searches ChromaDB for most relevant chunks
    for a given question
    """
    retriever = get_retriever(top_k=top_k)
    chunks = retriever.invoke(question)

    print(f"\n🔎 Retrieving chunks for: {question[:60]}")
    print(f"  📦 Found {len(chunks)} relevant chunks")

    return chunks


def generate_sub_questions(topic: str):
    """
    Uses Groq to break the main topic into
    specific sub questions for better retrieval
    """
    llm = get_llm()

    prompt = f"""You are a research assistant.
Break this research topic into 5 specific questions
that would help build a comprehensive research report.

Topic: "{topic}"

Return only the questions, one per line, nothing else."""

    response = llm.invoke(prompt)
    questions = response.content.strip().split("\n")
    questions = [q.strip() for q in questions if q.strip()]

    print(f"\n🧠 Generated sub questions:")
    for q in questions:
        print(f"  → {q}")

    return questions


def run_retrieval_agent(topic: str):
    """
    Main function — generates sub questions
    then retrieves relevant chunks for each
    """
    print(f"\n{'='*50}")
    print(f"🤖 Retrieval Agent Started")
    print(f"{'='*50}")

    # Step 1 — break topic into sub questions
    questions = generate_sub_questions(topic)

    # Step 2 — retrieve chunks for each question
    all_chunks = []
    seen_contents = set()

    for question in questions:
        chunks = retrieve_chunks(question)
        for chunk in chunks:
            if chunk.page_content not in seen_contents:
                all_chunks.append({
                    "question": question,
                    "content":  chunk.page_content,
                    "source":   chunk.metadata.get("source", "unknown")
                })
                seen_contents.add(chunk.page_content)

    print(f"\n✅ Retrieval Agent Complete!")
    print(f"📊 Total unique chunks retrieved: {len(all_chunks)}")
    return all_chunks