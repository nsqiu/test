from __future__ import annotations

import re
from difflib import SequenceMatcher
from typing import Iterable

from .types import NewsItem


WORD_RE = re.compile(r"\w+", re.UNICODE)


def _normalize_title(title: str) -> str:
    words = WORD_RE.findall(title.lower())
    return " ".join(words)


def deduplicate(items: Iterable[NewsItem], similarity_threshold: float = 0.9) -> list[NewsItem]:
    unique: list[NewsItem] = []
    seen_links: set[str] = set()

    for item in items:
        if not item.title:
            continue
        if item.link and item.link in seen_links:
            continue

        normalized = _normalize_title(item.title)
        is_duplicate = False
        for kept in unique:
            ratio = SequenceMatcher(None, normalized, _normalize_title(kept.title)).ratio()
            if ratio >= similarity_threshold:
                is_duplicate = True
                break

        if not is_duplicate:
            unique.append(item)
            if item.link:
                seen_links.add(item.link)

    return unique
