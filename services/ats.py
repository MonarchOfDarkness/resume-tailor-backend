import re
from collections import Counter

def ats_lint_text(text: str):
    issues = []
    lower = (text or "").lower()

    for h in ["experience", "education", "skills"]:
        if h not in lower:
            issues.append({"severity":"medium","issue":f"Missing '{h.upper()}' heading.","fix":f"Add a '{h.upper()}' heading."})

    if not re.search(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", text or ""):
        issues.append({"severity":"high","issue":"No email detected.","fix":"Add email near top."})

    if re.search(r"[•●▪◆◦]", text or ""):
        issues.append({"severity":"low","issue":"Special bullet characters detected.","fix":"Use '-' hyphen bullets."})

    words = re.findall(r"\b\w+\b", lower)
    if words:
        w, c = Counter(words).most_common(1)[0]
        if c > 80 and len(w) > 4:
            issues.append({"severity":"medium","issue":f"Possible keyword stuffing: '{w}' x{c}.","fix":"Reduce repetition; show evidence in bullets."})

    return {"issues": issues}
