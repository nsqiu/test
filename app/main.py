from __future__ import annotations

import argparse
from datetime import datetime, timezone

import yaml
from dateutil import parser as dt_parser

from .dedup import deduplicate
from .fetcher import fetch_rss
from .ranker import rank_items
from .report import build_markdown_report, save_report


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate daily finance news brief")
    p.add_argument("--sources", default="sources.yaml", help="Path to source config")
    p.add_argument("--max-items", type=int, default=10, help="Number of top news in report")
    p.add_argument(
        "--date",
        default="today",
        help="Report date, supports 'today' or yyyy-mm-dd",
    )
    return p.parse_args()


def load_sources(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}
    return config.get("sources", [])


def resolve_report_date(date_arg: str) -> datetime:
    if date_arg == "today":
        return datetime.now(timezone.utc)
    return dt_parser.parse(date_arg).replace(tzinfo=timezone.utc)


def main() -> None:
    args = parse_args()
    sources = load_sources(args.sources)

    all_items = []
    for src in sources:
        all_items.extend(
            fetch_rss(
                source_name=src["name"],
                url=src["url"],
                weight=float(src.get("weight", 1.0)),
            )
        )

    unique_items = deduplicate(all_items)
    ranked_items = rank_items(unique_items)[: args.max_items]

    report_date = resolve_report_date(args.date)
    report_md = build_markdown_report(ranked_items, report_date)
    output = save_report(report_md, report_date)

    print(f"Report generated: {output}")


if __name__ == "__main__":
    main()
