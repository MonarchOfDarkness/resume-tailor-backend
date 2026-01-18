import json
import os
from typing import Any, Dict, List

from google import genai

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

def tailor_resume_text(resume_text: str, jd_text: str, company_text: str) -> Dict[str, Any]:
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    prompt = f"""
You are a Resume Tailor Agent.

RULES:
- Do NOT invent experience, employers, degrees, certifications, dates, titles, or metrics.
- Keep ATS-friendly formatting: single column, standard headings, '-' bullets, no tables.
- If evidence is missing, put it in suggestions (do not add to resume).

OUTPUT:
Return ONLY valid JSON with this schema:
{{
  "tailored_text": "string",
  "change_log": ["string", ...],
  "suggestions": ["string", ...]
}}

JOB DESCRIPTION:
{(jd_text or "")[:12000]}

COMPANY CONTEXT:
{(company_text or "")[:8000]}

RESUME:
{(resume_text or "")[:20000]}
""".strip()

    resp = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config={"temperature": 0.4, "response_mime_type": "application/json"},
    )

    text = (resp.text or "").strip()

    # Parse JSON robustly
    try:
        data = json.loads(text)
    except Exception:
        s = text[text.find("{"): text.rfind("}") + 1] if "{" in text and "}" in text else "{}"
        data = json.loads(s) if s.strip() else {}

    return {
        "tailored_text": str(data.get("tailored_text", "")).strip(),
        "change_log": [str(x).strip() for x in data.get("change_log", []) if str(x).strip()] if isinstance(data.get("change_log"), list) else [],
        "suggestions": [str(x).strip() for x in data.get("suggestions", []) if str(x).strip()] if isinstance(data.get("suggestions"), list) else [],
    }
