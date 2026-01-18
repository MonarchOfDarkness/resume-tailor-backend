import re
from collections import Counter
from typing import Dict, List

_STOP = {
    "the","and","or","a","an","to","of","in","for","with","on","at","by","from","as","is","are","was","were",
    "this","that","these","those","it","its","be","been","being","will","would","can","could","should","may",
    "you","your","we","our","they","their","i","me","my","us","them","not","but","if","then","than","so",
    "about","into","over","under","within","across","per","via","using","use","used","based","including",
    "experience","years","year","role","team","work","working","ability","skills","skill","required","preferred",
}

def _tokens(text: str) -> List[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9\+\#\.\-]{1,}", (text or "").lower())
    return [w for w in words if w not in _STOP and len(w) > 2]

def compute_fit_score(jd_text: str, resume_text: str, top_n: int = 25) -> Dict:
    jd_tokens = _tokens(jd_text)
    res_lower = (resume_text or "").lower()

    if not jd_tokens:
        return {
            "score": 0,
            "present": [],
            "missing": [],
            "top_keywords": [],
            "note": "JD text missing or too short to score."
        }

    freq = Counter(jd_tokens)
    top_keywords = [w for w, _ in freq.most_common(top_n)]

    present = [k for k in top_keywords if k in res_lower]
    missing = [k for k in top_keywords if k not in res_lower]

    coverage = (len(present) / max(1, len(top_keywords)))  # 0..1

    # Simple scoring:
    # - Coverage (0..80)
    # - Bonus if resume contains standard headings (0..20)
    bonus = 0
    headings = ["summary", "skills", "experience", "education", "projects"]
    bonus += 4 * sum(1 for h in headings if h in res_lower)  # max 20

    score = int(round(min(100, coverage * 80 + bonus)))

    return {
        "score": score,
        "top_keywords": top_keywords,
        "present": present,
        "missing": missing,
        "coverage_ratio": round(coverage, 3),
        "heading_bonus": bonus,
    }

