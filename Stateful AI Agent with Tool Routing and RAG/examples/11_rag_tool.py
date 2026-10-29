"""Step 11: retrieval is a capability the agent may choose like any other tool."""

from _bootstrap import ROOT  # noqa: F401

from tools.knowledge_search import search_documents

if __name__ == "__main__":
    result = search_documents("How many annual leave days do full-time employees receive?")
    print("Retriever result:")
    for item in result["results"]:
        print(f"- {item['source']} (score={item.get('score', 'n/a')}): {item['content']}")

