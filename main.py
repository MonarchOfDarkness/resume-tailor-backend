from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from services.score import compute_fit_score
from pydantic import BaseModel
from pathlib import Path
from fastapi import Request
import uuid

from services.docx_parse import docx_bytes_to_text
from services.web_fetch import fetch_text
from services.ats import ats_lint_text
from services.tailor import tailor_resume_text
from services.docx_export import export_docx_bytes

app = FastAPI()

# CORS: for your Vercel frontend later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = Path("./data")
UPLOADS_DIR = DATA_DIR / "uploads"
EXPORTS_DIR = DATA_DIR / "exports"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

@app.get("/health")
def health():
    return {"status": "ok"}

# --- Upload ---
@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    data = await file.read()
    # Save file to disk
    file_id = str(uuid.uuid4())
    ext = Path(file.filename).suffix.lower() or ".docx"
    saved_path = UPLOADS_DIR / f"{file_id}{ext}"
    saved_path.write_bytes(data)

    return {"resume_id": file_id, "filename": file.filename}

class TailorRequest(BaseModel):
    resume_id: str
    jd_text: str | None = None
    jd_url: str | None = None
    company_url: str | None = None

# --- Tailor ---
@app.post("/tailor")
def tailor(req: TailorRequest):
    # Load resume bytes
    resume_path = next(UPLOADS_DIR.glob(f"{req.resume_id}.*"), None)
    if resume_path is None:
        return {"error": "resume_id not found"}

    resume_bytes = resume_path.read_bytes()
    resume_text = docx_bytes_to_text(resume_bytes)

    # Get JD + company
    jd = req.jd_text or (fetch_text(req.jd_url) if req.jd_url else "")
    fit = compute_fit_score(jd_text=jd, resume_text=resume_text)
    company = fetch_text(req.company_url) if req.company_url else ""

    ats_before = ats_lint_text(resume_text)

    result = tailor_resume_text(
        resume_text=resume_text,
        jd_text=jd,
        company_text=company,
    )

    ats_after = ats_lint_text(result["tailored_text"])

    return {
        "tailored_text": result["tailored_text"],
        "change_log": result["change_log"],
        "suggestions": result["suggestions"],
        "ats_before": ats_before,
        "ats_after": ats_after,
        "fit_score": fit,
    }

class ExportRequest(BaseModel):
    filename: str = "tailored_resume.docx"
    title: str = "TAILORED RESUME"
    content: str

# --- Export ---
@app.post("/export")
def export(req: ExportRequest, request: Request):
    data = export_docx_bytes(req.title, req.content)
    out_path = EXPORTS_DIR / f"{uuid.uuid4()}_{req.filename}"
    out_path.write_bytes(data)

    # For now: return local path (we'll switch to cloud storage later)
    base = str(request.base_url).rstrip("/")
    return {
    "saved_to": str(out_path),
    "download_url": f"{base}/download/{out_path.name}",
}



@app.get("/download/{filename}")
def download(filename: str):
    file_path = EXPORTS_DIR / filename
    if not file_path.exists():
        return {"error": "file not found"}
    return FileResponse(
        path=str(file_path),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=filename,
    )
