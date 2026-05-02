import requests
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from core.vector_store import get_vector_store

def fetch_page(url: str):
    """
    Fetches full text content from a URL
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # remove junk tags
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)

        # remove empty lines
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        clean_text = "\n".join(lines)

        print(f"  ✅ Fetched: {url[:60]}...")
        return clean_text

    except Exception as e:
        print(f"  ❌ Failed: {url[:60]} — {e}")
        return None


def chunk_text(text: str, source_url: str):
    """
    Splits text into chunks with metadata
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.create_documents(
        texts=[text],
        metadatas=[{"source": source_url}]
    )

    return chunks


def store_chunks(chunks: list):
    """
    Stores chunks in ChromaDB
    """
    vector_store = get_vector_store()
    vector_store.add_documents(chunks)
    return len(chunks)


def run_reader_agent(sources: list):
    """
    Main function — fetches, chunks, and stores all sources
    """
    print(f"\n{'='*50}")
    print(f"🤖 Reader Agent Started")
    print(f"{'='*50}")

    total_chunks = 0

    for i, source in enumerate(sources):
        url   = source["url"]
        title = source["title"]

        print(f"\n📄 Processing {i+1}/{len(sources)}: {title[:50]}")

        # Step 1 — fetch full page content
        text = fetch_page(url)
        if not text:
            continue

        # Step 2 — chunk the text
        chunks = chunk_text(text, url)
        print(f"  📦 Chunks created: {len(chunks)}")

        # Step 3 — store in ChromaDB
        stored = store_chunks(chunks)
        total_chunks += stored
        print(f"  💾 Stored in ChromaDB: {stored} chunks")

    print(f"\n✅ Reader Agent Complete!")
    print(f"📊 Total chunks stored: {total_chunks}")
    return total_chunks