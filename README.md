# Resume Tailor Backend

AI-powered backend service for tailoring resumes to specific job descriptions, optimizing for ATS (Applicant Tracking Systems), and exporting polished documents.

Deployed on **Google Cloud Run**.

---

## ✨ Features

- Resume tailoring using **Google Gemini API**
- Job description analysis (URL or pasted text)
- ATS compatibility checks (before & after)
- Job fit scoring (keywords, coverage, gaps)
- DOCX export of tailored resumes
- Stateless, production-ready API

---

## 🧠 Architecture

- **Framework:** FastAPI
- **AI Model:** Google Gemini
- **Deployment:** Google Cloud Run
- **Frontend:** Next.js (Vercel)
- **Language:** Python 3.12+

---

## 📁 Project Structure

```
resume-tailor-backend/
├── main.py              # FastAPI entry point
├── services/            # Resume parsing, scoring, ATS logic
├── requirements.txt     # Python dependencies
├── Dockerfile           # Cloud Run container build
└── README.md
```

---

## 🚀 API Endpoints

### `POST /upload`
Upload a `.docx` resume.

### `POST /tailor`
Tailor the resume to a job description.

**Input**
```json
{
  "resume_id": "string",
  "jd_url": "optional",
  "jd_text": "optional",
  "company_url": "optional"
}
```

**Output**
```json
{
  "tailored_text": "...",
  "change_log": [],
  "suggestions": [],
  "ats_before": {},
  "ats_after": {},
  "fit_score": {}
}
```

---

### `POST /export`
Export the tailored resume as a `.docx`.

---

## 🔐 Environment Variables

Configured in **Cloud Run**, not committed to GitHub.

```
GEMINI_API_KEY=your_api_key_here
```

---

## 🛠 Local Development

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## ☁️ Deployment

Deployed using **Google Cloud Run** via container builds.

This repository is used for **source control only** — deployments are handled through Google Cloud.

---

## 📌 Notes

- Generated files (exports, temp data) are excluded from version control
- Authentication and persistence are handled by the frontend
- Designed to be stateless and horizontally scalable


