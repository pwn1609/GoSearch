import re
from dataclasses import dataclass

from bs4 import BeautifulSoup


@dataclass
class ParsedPage:
    url: str
    title: str
    description: str
    body_text: str


def parse_page(url: str, html: str) -> ParsedPage:
    soup = BeautifulSoup(html, "lxml")

    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.strip()

    description = ""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        description = meta["content"].strip()

    body_text = ""
    body = soup.find("body")
    if body:
        body_text = re.sub(r"\s+", " ", body.get_text(separator=" ")).strip()

    return ParsedPage(url=url, title=title, description=description, body_text=body_text)
