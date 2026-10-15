import json
import re
from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup

PAGE_URL = "https://www.ampublic.com/frequently-asked-questions/"
RAW_FILE = Path("data/raw/faq.html")
OUTPUT_FILE = Path("data/faq.json")

AUDIENCES = {
    "individuals": "Individuals",
    "groups": "Groups",
    "broker": "Brokers",
    "provider": "Providers",
}


def clean_text(element):
    """Get an element's text on one line, without stray spaces before punctuation."""
    text = element.get_text(" ", strip=True)
    return re.sub(r"\s+([.,;:!?)])", r"\1", text)


def answer_to_text(body):
    """Convert an answer's HTML into plain text, keeping link URLs."""
    for link in body.find_all("a"):
        href = link.get("href", "")
        if href.startswith("http"):
            link.replace_with(f"{link.get_text(strip=True)} ({href})")

    blocks = body.find_all(["p", "li"])
    if not blocks:
        return clean_text(body)

    lines = []
    for block in blocks:
        text = clean_text(block)
        if text:
            prefix = "- " if block.name == "li" else ""
            lines.append(prefix + text)
    return "\n".join(lines)


def main():
    soup = BeautifulSoup(RAW_FILE.read_text(encoding="utf-8"), "html.parser")
    records = []

    for audience_id, audience_name in AUDIENCES.items():
        block = soup.find(id=audience_id)
        if block is None:
            raise SystemExit(f"Section id='{audience_id}' not found. Has the page changed?")

        for item in block.find_all(class_="section"):
            heading = item.find("h3")
            body = item.find(class_="section-body")
            if heading is None or body is None:
                print(f"Skipping an item in {audience_name}: missing question or answer")
                continue

            records.append({
                "audience": audience_name,
                "question": clean_text(heading),
                "answer": answer_to_text(body),
                "url": f"{PAGE_URL}#{heading.get('id', '')}",
            })

    OUTPUT_FILE.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Saved {len(records)} Q&A pairs to {OUTPUT_FILE}")
    for audience, count in Counter(r["audience"] for r in records).items():
        print(f"  {audience}: {count}")


if __name__ == "__main__":
    main()