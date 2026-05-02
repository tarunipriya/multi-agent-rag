import os
from dotenv import load_dotenv

load_dotenv()

groq_key   = os.getenv("GROQ_API_KEY")
tavily_key = os.getenv("TAVILY_API_KEY")

print("Groq key loaded:   ", "✅" if groq_key   else "❌ Missing")
print("Tavily key loaded: ", "✅" if tavily_key else "❌ Missing")

try:
    import langchain, chromadb
    from sentence_transformers import SentenceTransformer
    from tavily import TavilyClient
    from groq import Groq
    print("All libraries imported: ✅")
except ImportError as e:
    print(f"Missing library: ❌ {e}")

try:
    from groq import Groq
    client = Groq(api_key=groq_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "Say hello in 5 words."}]
    )
    print("Groq connected:         ✅", response.choices[0].message.content)
except Exception as e:
    print(f"Groq connection: ❌ {e}")

try:
    from tavily import TavilyClient
    tavily = TavilyClient(api_key=tavily_key)
    tavily.search("artificial intelligence", max_results=1)
    print("Tavily connected:       ✅")
except Exception as e:
    print(f"Tavily connection: ❌ {e}")

try:
    import chromadb
    client = chromadb.Client()
    client.create_collection("test")
    print("ChromaDB working:       ✅")
except Exception as e:
    print(f"ChromaDB: ❌ {e}")