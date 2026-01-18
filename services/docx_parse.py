import io
from docx import Document

def docx_bytes_to_text(data: bytes, max_chars: int = 60000) -> str:
    doc = Document(io.BytesIO(data))
    lines = [p.text.strip() for p in doc.paragraphs if p.text and p.text.strip()]
    return "\n".join(lines)[:max_chars]
