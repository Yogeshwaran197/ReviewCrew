from pydantic import BaseModel
from typing import TypedDict, Dict, Literal


class Finding(BaseModel):
    file: str
    line: int
    severity: Literal["low", "medium", "high", "critical"]
    issue: str
    suggestion: str