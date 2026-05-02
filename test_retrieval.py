from agents.retrieval_agent import run_retrieval_agent

chunks = run_retrieval_agent('Impact of AI on healthcare 2024')
print(f'Done! {len(chunks)} chunks retrieved')
print(f'Sample chunk: {chunks[0]["content"][:200]}')