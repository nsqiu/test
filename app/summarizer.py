from __future__ import annotations

import re

from .types import NewsItem


SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?。！？])\s+")


def summarize_item(item: NewsItem, max_sentences: int = 2) -> str:
    text = re.sub(r"<[^>]+>", "", item.summary).strip()
    if not text:
        return "暂无摘要，建议点击原文查看细节。"

    sentences = [s.strip() for s in SENTENCE_SPLIT_RE.split(text) if s.strip()]
    if not sentences:
        return text[:120]

    return " ".join(sentences[:max_sentences])
