from __future__ import annotations

from datetime import datetime
from pathlib import Path

from .summarizer import summarize_item
from .types import NewsItem


def build_markdown_report(items: list[NewsItem], report_date: datetime) -> str:
    lines: list[str] = []
    title = report_date.strftime("财经日报 - %Y-%m-%d")

    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"共收录 {len(items)} 条重点新闻。")
    lines.append("")

    for idx, item in enumerate(items, start=1):
        pub_time = item.published_at.astimezone().strftime("%H:%M")
        lines.append(f"## {idx}. {item.title}")
        lines.append(f"- 来源：{item.source} | 时间：{pub_time} | 评分：{item.score}")
        lines.append(f"- 摘要：{summarize_item(item)}")
        lines.append(f"- 链接：{item.link or 'N/A'}")
        lines.append("")

    return "\n".join(lines)


def save_report(content: str, report_date: datetime, out_dir: str = "output") -> Path:
    path = Path(out_dir)
    path.mkdir(parents=True, exist_ok=True)
    filename = f"daily_{report_date.strftime('%Y%m%d')}.md"
    output_path = path / filename
    output_path.write_text(content, encoding="utf-8")
    return output_path
