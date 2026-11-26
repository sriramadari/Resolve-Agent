import json
import time
from pathlib import Path

import httpx

from app.ingestion import clean_markdown

SOURCES = Path("data/sources.txt")
OUTPUT = Path("data/raw/docs.jsonl")


def main() -> None:
    urls = [
        line.strip()
        for line in SOURCES.read_text().splitlines()
        if line.strip() and not line.startswith("#")
    ]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    saved = 0
    with OUTPUT.open("w", encoding="utf-8") as out, httpx.Client(timeout=20, follow_redirects=True) as client:
        for url in urls:
            try:
                response = client.get(url)
                response.raise_for_status()
            except httpx.HTTPError as e:
                print(f"SKIP {url}: {e}")
                continue

            title, text = clean_markdown(response.text)
            record = {"url": url.removesuffix(".md"), "title": title, "text": text}
            out.write(json.dumps(record) + "\n")
            saved += 1
            print(f"OK   {title} ({len(text)} chars)")
            time.sleep(1)

    print(f"\nSaved {saved} of {len(urls)} pages to {OUTPUT}")


if __name__ == "__main__":
    main()