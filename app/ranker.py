from __future__ import annotations

from datetime import datetime, timezone

from .types import NewsItem


KEYWORDS = {
    "rate": 1.2,
    "inflation": 1.2,
    "fed": 1.1,
    "earnings": 1.0,
    "guidance": 1.0,
    "default": 1.3,
    "regulation": 0.9,
    "gdp": 1.0,
    "oil": 0.8,
    "tariff": 1.1,
}


def score_item(item: NewsItem, now: datetime | None = None) -> float:
    now = now or datetime.now(timezone.utc)
    age_hours = max((now - item.published_at).total_seconds() / 3600.0, 0)
    freshness = max(0.0, 1.5 - age_hours / 24.0)

    lowered = f"{item.title} {item.summary}".lower()
    keyword_score = sum(weight for key, weight in KEYWORDS.items() if key in lowered)

    score = item.source_weight * 1.5 + freshness + keyword_score
    return round(score, 3)


def rank_items(items: list[NewsItem]) -> list[NewsItem]:
    for item in items:
        item.score = score_item(item)
    return sorted(items, key=lambda x: x.score, reverse=True)
