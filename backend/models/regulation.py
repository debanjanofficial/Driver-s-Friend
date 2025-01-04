from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class Regulation:
    category: str
    country: str
    content: str
    language: str
    keywords: List[str]
    last_updated: datetime
    source: str
    fine_amount: Optional[float] = None
