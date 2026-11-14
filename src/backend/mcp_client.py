import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient


ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError(f"GITHUB_TOKEN not found. Looked in: {ROOT / '.env'}")


async def client():

    client = MultiServerMCPClient({
        "github": {
            "transport": "http",
            "url": "https://api.githubcopilot.com/mcp/",
            "headers": {"Authorization": f"Bearer {GITHUB_TOKEN}"}
             }
    })


    tools = await client.get_tools()

    READ_TOOLS = {"pull_request_read", "get_file_contents", "search_code"}

    tool_map = {t.name : t for t in tools}

    pull_request_read  = tool_map["pull_request_read"]
    get_file_content = tool_map["get_file_contents"]
    search_code = tool_map["search_code"]

    file_content = await get_file_content.ainvoke({
        "owner": "Yogeshwaran197",
        "repo": "HybridRAG-Agent-Self-Reflective-RAG-with-Reranking-Live-Web-Search",
        "path": "/"
    })

    print(f"File Content : {file_content}\n\n")

    pull_request_read = await pull_request_read.ainvoke({
        "owner": "Yogeshwaran197",
        "repo": "HybridRAG-Agent-Self-Reflective-RAG-with-Reranking-Live-Web-Search",
        "method": "get_files",
        "pullNumber": 1,
    })

    print(f"PULL Request : {pull_request_read}\n\n")

    search_code = await search_code.ainvoke({
        "query" : "where is websearch ?"
    })

    print(f"search_code : {search_code}")

    



if __name__ == "__main__":
    asyncio.run(client())