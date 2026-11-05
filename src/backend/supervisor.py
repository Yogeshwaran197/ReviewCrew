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
from langgraph.types import Command, interrupt
from typing import TypedDict
from pydantic import BaseModel


load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("INVALID API KEY")

llm =  ChatGroq(
    model = "openai/gpt-oss-20b",
    api_key=GROQ_API_KEY
)

