from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Corpus(BaseModel):
    id: int
    reference: str


class Text(BaseModel):
    id: int
    title: str
    author: str
    date: Optional[datetime]
    raw_text: str
    corpus: Corpus
