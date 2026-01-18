import re
import requests
from bs4 import BeautifulSoup

def fetch_text(url: str, max_chars: int = 20000) -> str:
    if not url:
        return ""
    r = requests.get(url, timeout=20, headers={"User-Agent": "ResumeTailor/1.0"})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    for t in soup(["script", "style", "noscript", "svg"]):
        t.decompose()
    text = soup.get_text("\n")
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text[:max_chars]
