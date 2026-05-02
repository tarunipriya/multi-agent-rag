from agents.search_agent import run_search_agent
from agents.reader_agent import run_reader_agent
from agents.retrieval_agent import run_retrieval_agent
from agents.synthesis_agent import run_synthesis_agent

def run_research_pipeline(topic: str):
    """
    Orchestrates all 4 agents to produce
    a complete research report
    """
    print(f"\n{'='*50}")
    print(f"🚀 Research Pipeline Started")
    print(f"📌 Topic: {topic}")
    print(f"{'='*50}")

    # Agent 1 — search web
    print(f"\n⚡ Running Agent 1 — Web Search...")
    sources = run_search_agent(topic)

    # Agent 2 — read and store
    print(f"\n⚡ Running Agent 2 — Document Reader...")
    total_chunks = run_reader_agent(sources)

    # Agent 3 — retrieve relevant chunks
    print(f"\n⚡ Running Agent 3 — RAG Retrieval...")
    chunks = run_retrieval_agent(topic)

    # Agent 4 — synthesize report
    print(f"\n⚡ Running Agent 4 — Synthesis...")
    report = run_synthesis_agent(topic, chunks)

    print(f"\n{'='*50}")
    print(f"✅ Pipeline Complete!")
    print(f"{'='*50}")

    return {
        "topic":        topic,
        "sources":      sources,
        "total_chunks": total_chunks,
        "report":       report
    }