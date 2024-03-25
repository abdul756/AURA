from typing import List
import pathway as pw

class QueryInputSchema(pw.Schema):
    query: str
    user: str
    difficulty_level: str
    context_keywords: List[str]
    mode: str

class DataInputSchema(pw.Schema):
    summary: str