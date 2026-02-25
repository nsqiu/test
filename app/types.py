from dataclasses import dataclass
from datetime import datetime


@dataclass
class NewsItem:
    source: str
    source_weight: float
    title: str
    link: str
    published_at: datetime
    summary: str
    score: float = 0.0
