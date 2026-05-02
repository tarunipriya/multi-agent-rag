# 🔬 Multi-Agent RAG Research System

A production-level AI research system that uses multiple specialized agents to automatically search the web, read documents, retrieve relevant information, and generate comprehensive research reports.

## 🤖 The 4 Agents

| Agent | Role | Tool |
|---|---|---|
| Agent 1 | Web Search | Tavily API |
| Agent 2 | Document Reader | BeautifulSoup + LangChain |
| Agent 3 | RAG Retrieval | ChromaDB + sentence-transformers |
| Agent 4 | Synthesis | Groq (Llama 3.3 70B) |

## 🧱 Tech Stack
- **LLM:** Groq (llama-3.3-70b-versatile) — Free
- **Embeddings:** sentence-transformers — Free, Local
- **Vector DB:** ChromaDB — Free, Local
- **Web Search:** Tavily API — Free tier
- **Framework:** LangChain
- **UI:** Streamlit
- **API:** FastAPI

## ⚙️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/tarunipriya/multi-agent-rag.git
cd multi-agent-rag
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add API keys
Create a `.env` file:
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here

### 5. Run Streamlit UI
```bash
streamlit run app.py
```

### 6. Run FastAPI
```bash
python api.py
```

## 🌐 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API info |
| GET | `/health` | Health check |
| POST | `/research` | Run research pipeline |
