import streamlit as st
from orchestrator import run_research_pipeline

# page config
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔬",
    layout="wide"
)

# title
st.title("🔬 Multi-Agent Research System")
st.markdown("Powered by **Groq + Tavily + ChromaDB + LangChain**")
st.divider()

# sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    st.markdown("**Model:** llama-3.3-70b-versatile")
    st.markdown("**Embeddings:** all-MiniLM-L6-v2")
    st.markdown("**Vector DB:** ChromaDB")
    st.markdown("**Search:** Tavily")
    st.divider()
    st.markdown("### How it works")
    st.markdown("1. 🔍 Agent 1 searches the web")
    st.markdown("2. 📄 Agent 2 reads full pages")
    st.markdown("3. 🧩 Agent 3 retrieves chunks")
    st.markdown("4. ✍️ Agent 4 writes report")

# main area
topic = st.text_input(
    "Enter your research topic:",
    placeholder="e.g. Impact of AI on healthcare 2024"
)

run_button = st.button("🚀 Run Research", type="primary")

if run_button and topic:
    st.divider()

    # progress tracking
    progress = st.progress(0)
    status   = st.empty()

    with st.spinner("🤖 Agents are working..."):

        # agent 1
        status.markdown("⚡ **Agent 1** — Searching the web...")
        progress.progress(10)

        from agents.search_agent import run_search_agent
        sources = run_search_agent(topic)
        progress.progress(25)
        st.success(f"✅ Agent 1 Complete — {len(sources)} sources found")

        # agent 2
        status.markdown("⚡ **Agent 2** — Reading pages...")
        progress.progress(35)

        from agents.reader_agent import run_reader_agent
        total_chunks = run_reader_agent(sources)
        progress.progress(55)
        st.success(f"✅ Agent 2 Complete — {total_chunks} chunks stored")

        # agent 3
        status.markdown("⚡ **Agent 3** — Retrieving relevant chunks...")
        progress.progress(65)

        from agents.retrieval_agent import run_retrieval_agent
        chunks = run_retrieval_agent(topic)
        progress.progress(80)
        st.success(f"✅ Agent 3 Complete — {len(chunks)} chunks retrieved")

        # agent 4
        status.markdown("⚡ **Agent 4** — Writing report...")
        progress.progress(90)

        from agents.synthesis_agent import run_synthesis_agent
        report = run_synthesis_agent(topic, chunks)
        progress.progress(100)
        st.success(f"✅ Agent 4 Complete — Report ready!")

    status.markdown("✅ **All agents complete!**")
    st.divider()

    # display report
    st.markdown("## 📄 Research Report")
    st.markdown(report)
    st.divider()

    # display sources
    with st.expander("🌐 View All Sources"):
        for i, source in enumerate(sources):
            st.markdown(f"**{i+1}. [{source['title']}]({source['url']})**")
            st.markdown(f"_{source['snippet'][:200]}..._")
            st.divider()

    # download button
    st.download_button(
        label="⬇️ Download Report",
        data=report,
        file_name=f"research_{topic[:30].replace(' ','_')}.md",
        mime="text/markdown"
    )

elif run_button and not topic:
    st.warning("⚠️ Please enter a research topic first!")