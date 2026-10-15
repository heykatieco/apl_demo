from pathlib import Path

import requests

URL = "https://www.ampublic.com/frequently-asked-questions/"
OUTPUT_FILE = Path("data/raw/faq.html")

response = requests.get(
    URL,
    headers={"User-Agent": "apl-faq-bot (personal portfolio project)"},
    timeout=30,
)
response.raise_for_status()

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE.write_text(response.text, encoding="utf-8")

print(f"Status code: {response.status_code}")
print(f"Saved {len(response.text):,} characters to {OUTPUT_FILE}")