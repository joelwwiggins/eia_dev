from pydantic import BaseModel
from typing import List, Optional

class EIAData(BaseModel):
    category: str
    year: int
    data: List[dict]

class EIAResponse(BaseModel):
    response: EIAData
    status: str
    message: Optional[str] = None

class QueryParameters(BaseModel):
    category: str
    year: int