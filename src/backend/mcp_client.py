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

    
class GitHubTools:

    def __init__(self):
        self.client = MultiServerMCPClient({
        "github": {
            "transport": "http",
            "url": "https://api.githubcopilot.com/mcp/",
            "headers": {"Authorization": f"Bearer {GITHUB_TOKEN}"}
             }
        })

        self.tool_map = {}  


    async def connect(self):
        tools = await self.client.get_tools()
        read_tools = {"pull_request_read", "get_file_contents", "search_code"}
        self.tool_map = {t.name: t for t in tools if t.name in read_tools}


    async def get_pr(self, owner: str, repo: str, pr_number: int, method: str = "get_files"):
         return await self.tool_map["pull_request_read"].ainvoke({
            "method": method,
            "owner": owner,
            "repo": repo,
            "pullNumber": pr_number,
        })

    async def read_file(self, owner: str, repo: str, path: str):
         return await self.tool_map["get_file_contents"].ainvoke({
            "owner": owner,
            "repo": repo,
            "path": path,
        })

    async def search_code(self, query: str):
       return await self.tool_map["search_code"].ainvoke({
            "query": query,
        })

    
    async def main():
        owner = "Yogeshwaran197"
        repo = "HybridRAG-Agent-Self-Reflective-RAG-with-Reranking-Live-Web-Search"

        gh = GitHubTools()
        await gh.connect()

        print("FILES:", await gh.read_file(owner, repo, "/"), "\n")
        print("PR:", await gh.get_pr(owner, repo, 1, "get_files"), "\n")
        print("SEARCH:", await gh.search_code(f"websearch repo:{owner}/{repo}"))


if __name__ == "__main__":
        asyncio.run(GitHubTools.main())