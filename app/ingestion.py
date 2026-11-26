import re

def clean_markdown(raw: str) -> tuple[str, str]:
    lines = raw.splitlines()
    start = next((i for i, line in enumerate(lines) if line.startswith("# ")), 0)
    lines = lines[start:]
    if not lines:
        return "Untitled", ""

    title = lines[0][2:].strip() if lines[0].startswith("# ") else "Untitled"
    text = "\n".join(lines)

    text = re.sub(r"<img[^>]*>", "", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"<li>", "\n- ", text)
    text = re.sub(r"</?[A-Za-z][^>]*>", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return title, text.strip()


def chunk_markdown(text: str, max_chars: int = 1500, overlap_chars: int = 200) -> list[str]:
    sections = re.split(r"\n(?=#{1,3} )", text)
    chunks = []

    for section in sections:
        first_line = section.splitlines()[0] if section else ""
        heading = first_line if first_line.startswith("#") else ""
        paragraphs = [p.strip() for p in section.split("\n\n") if p.strip()]

        current = ""
        for paragraph in paragraphs:
            if current and len(current) + len(paragraph) > max_chars:
                chunks.append(current)
                tail = current[-overlap_chars:]
                current = f"{heading}\n...{tail}" if heading else tail
            current = f"{current}\n\n{paragraph}" if current else paragraph

        if current:
            chunks.append(current)

    return [c for c in chunks if len(c) > 40]

