from __future__ import annotations

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Iterable

import feedparser

from .types import NewsItem


def _parse_datetime(entry) -> datetime:
    raw = entry.get("published") or entry.get("updated")
    if raw:
        try:
            dt = parsedate_to_datetime(raw)
            if dt.tzinfo is None:
                return dt.replace(tzinfo=timezone.utc)
            return dt
        except (TypeError, ValueError):
            pass
    return datetime.now(timezone.utc)


def fetch_rss(source_name: str, url: str, weight: float) -> Iterable[NewsItem]:
    feed = feedparser.parse(url)
    for entry in feed.entries:
        yield NewsItem(
            source=source_name,
            source_weight=weight,
            title=(entry.get("title") or "").strip(),
            link=(entry.get("link") or "").strip(),
            published_at=_parse_datetime(entry),
            summary=(entry.get("summary") or entry.get("description") or "").strip(),
        )
