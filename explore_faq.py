from pathlib import Path

from bs4 import BeautifulSoup

html = Path("data/raw/faq.html").read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")

for audience_id in ["individuals", "groups", "broker", "provider"]:
    block = soup.find(id=audience_id)
    if block is None:
        print(f"{audience_id}: NOT FOUND")
    else:
        items = block.find_all(class_="section")
        print(f"{audience_id}: {len(items)} items")

first_item = soup.find(id="individuals").find(class_="section")
print("\n----- First item's HTML -----\n")
print(first_item.prettify()[:2000])