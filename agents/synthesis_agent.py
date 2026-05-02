from core.llm import get_llm

def run_synthesis_agent(topic: str, chunks: list):
    """
    Takes all retrieved chunks and writes
    a structured research report with citations
    """
    print(f"\n{'='*50}")
    print(f"🤖 Synthesis Agent Started")
    print(f"{'='*50}")

    llm = get_llm()

    # build context from all chunks
    context = ""
    sources = set()
    for i, chunk in enumerate(chunks):
        context += f"\n[{i+1}] {chunk['content']}\n"
        sources.add(chunk['source'])

    print(f"\n📚 Building report from {len(chunks)} chunks...")
    print(f"🌐 Sources used: {len(sources)}")

    prompt = f"""You are an expert research analyst.
Write a comprehensive, well-structured research report on the topic below.
Use ONLY the context provided. Cite sources using [1], [2] etc.

Topic: {topic}

Context:
{context}

Write the report in this exact format:

# {topic}

## Executive Summary
(3-4 sentences summarizing the key findings)

## Key Finding 1 · (give it a title)
(detailed paragraph with citations)

## Key Finding 2 · (give it a title)
(detailed paragraph with citations)

## Key Finding 3 · (give it a title)
(detailed paragraph with citations)

## Key Finding 4 · (give it a title)
(detailed paragraph with citations)

## Challenges and Risks
(paragraph about challenges with citations)

## Conclusion
(2-3 sentences wrapping up)

## Sources
(list all sources used)
"""

    print(f"\n✍️  Writing report...")
    response = llm.invoke(prompt)
    report = response.content

    print(f"\n✅ Synthesis Agent Complete!")
    print(f"📄 Report length: {len(report)} characters")

    return report