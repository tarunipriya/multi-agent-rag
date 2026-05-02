import os
from dotenv import load_dotenv
from tavily import TavilyClient
from core.llm import get_llm

load_dotenv()

def search_web(topic: str, num_results: int = 10):
    """
    Searches the web for a given topic
    Returns list of URLs and snippets
    """
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    print(f"\n🔍 Searching web for: {topic}")

    results = client.search(
        query=topic,
        max_results=num_results,
        search_depth="advanced"
    )

    sources = []
    for r in results["results"]:
        sources.append({
            "title":   r.get("title",   ""),
            "url":     r.get("url",     ""),
            "snippet": r.get("content", "")
        })
        print(f"  ✅ Found: {r.get('title', '')}")

    print(f"\n📋 Total sources found: {len(sources)}")
    return sources


def refine_query(topic: str):
    """
    Uses Groq to generate better search queries
    from the user's topic
    """
    llm = get_llm()

    prompt = f"""You are a research assistant.
Generate 3 specific search queries for this topic: "{topic}"
Return only the queries, one per line, nothing else."""

    response = llm.invoke(prompt)
    queries = response.content.strip().split("\n")
    queries = [q.strip() for q in queries if q.strip()]

    print(f"\n🧠 Refined queries:")
    for q in queries:
        print(f"  → {q}")

    return queries


def run_search_agent(topic: str):
    """
    Main function — refines query then searches web
    Returns all sources found
    """
    print(f"\n{'='*50}")
    print(f"🤖 Search Agent Started")
    print(f"{'='*50}")

    # Step 1 — refine the topic into better queries
    queries = refine_query(topic)

    # Step 2 — search web for each query
    all_sources = []
    seen_urls = set()

    for query in queries:
        results = search_web(query, num_results=5)
        for r in results:
            if r["url"] not in seen_urls:
                all_sources.append(r)
                seen_urls.add(r["url"])

    print(f"\n✅ Search Agent Complete — {len(all_sources)} unique sources found")
    return all_sources