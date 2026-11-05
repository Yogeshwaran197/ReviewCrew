import os
import psycopg
from  dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg import connect
from psycopg.rows import dict_row
from langgraph.types import Command, interrupt, Literal,Optional
from typing import TypedDict
from pydantic import BaseModel
from src.agents.doc_agent import DocIssue
from src.agents.reviewer_agent import Finding
from src.agents.tester_agent import TestCase


load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("INVALID API KEY")

llm =  ChatGroq(
    model = "openai/gpt-oss-20b",
    api_key=GROQ_API_KEY
)


class CriticVerdict(BaseModel):
    agent: Literal["reviewer", "tester", "doc_writer"]
    approved: bool
    feedback: str = ""


class AgentState(TypedDict):

    pr_url: str
    context_pack: str
    error: str

    #supervisor       
    agents_to_run: list[str]      

    #workers(agents)
    findings: list[Finding]       
    tests: list[TestCase]          
    doc_issues: list[DocIssue]     

    #iteration
    verdicts: list[CriticVerdict]
    retry_count : int 

    #human in a loop   
    human_decision: Literal["approve", "reject"]





