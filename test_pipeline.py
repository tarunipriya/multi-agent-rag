from orchestrator import run_research_pipeline

topic = "Impact of AI on healthcare 2024"
result = run_research_pipeline(topic)

print("\n" + "="*50)
print("FINAL RESEARCH REPORT")
print("="*50)
print(result["report"])

# save report to file
with open("report.md", "w", encoding="utf-8") as f:
    f.write(result["report"])

print("\n✅ Report saved to report.md")