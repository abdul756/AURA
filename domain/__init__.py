from typing import List, Optional
from pydantic import BaseModel

class QueryInputSchema(BaseModel):
    query: str
    user: str
    difficulty_level: Optional[str] = "medium"
    context_keywords: List[str] = []
