from pydantic import BaseModel
from typing import TypedDict, Dict, Literal


class TestCase(BaseModel):
    target_function: str
    file: str
    code: str

