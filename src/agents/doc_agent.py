from pydantic import BaseModel
from typing import TypedDict, Dict, Literal


class DocIssue(BaseModel):
    file: str
    problem: str
    suggested_fix: str