"""
Router: /api/bulk-generate  &  /api/bulk-status/{job_id}
Handles Excel / CSV / Google-Sheets bulk processing pipeline.
"""
import os
import re
import shutil
import uuid
import urllib.request

from fastapi import APIRouter, BackgroundTasks, File, Form, HTTPException, UploadFile
from pathlib import Path

from app.services.bulk_processor import process_excel_background, get_job_status

router = APIRouter(prefix="/api", tags=["Bulk"])


# ── Start bulk job ─────────────────────────────────────────────────────────────

@router.post("/bulk-generate")
async def start_bulk_generation(
    background_tasks: BackgroundTasks,
    category: str           = Form(...),
    file:     UploadFile | None = File(None),
    url:      str | None    = Form(None),
):
    """
    Kick off a bulk image-generation job in the background.

    Accepts one of:
    - **file**: An Excel (.xlsx / .xls) or CSV file with product rows
    - **url**:  A public Google Sheets URL  *or*  a direct image URL (creates a 1-row job)

    Returns a **job_id** that can be polled via `/api/bulk-status/{job_id}`.
    """
    try:
        if not file and not url:
            raise HTTPException(
                status_code=400,
                detail="Must provide an Excel file or a Google Sheets URL.",
            )

        temp_dir = Path("outputs") / "temp_excel"
        temp_dir.mkdir(parents=True, exist_ok=True)

        # ── Google Sheets URL ──────────────────────────────────────────────
        if url and "docs.google.com/spreadsheets" in url:
            match = re.search(r"/d/([a-zA-Z0-9-_]+)", url)
            if not match:
                raise HTTPException(
                    status_code=400,
                    detail="Could not extract document ID from the Google Sheets URL.",
                )
            doc_id          = match.group(1)
            job_id          = doc_id
            csv_export_url  = f"https://docs.google.com/spreadsheets/d/{doc_id}/export?format=csv"
            file_path       = temp_dir / f"{job_id}_sheet.csv"

            if not file_path.exists():
                urllib.request.urlretrieve(csv_export_url, file_path)

        # ── Uploaded file ─────────────────────────────────────────────────
        elif file:
            if not file.filename.endswith((".xlsx", ".xls", ".csv")):
                raise HTTPException(
                    status_code=400,
                    detail="Uploaded file must be an Excel (.xlsx/.xls) or CSV file.",
                )
            base_filename = os.path.splitext(file.filename)[0]
            job_id = (
                "".join(c for c in base_filename if c.isalnum() or c in (" ", "_", "-"))
                .replace(" ", "_")
                .lower()
            )
            safe_filename = "".join(
                c for c in file.filename if c.isalnum() or c in (".", "_", "-")
            )
            file_path = temp_dir / safe_filename
            with open(file_path, "wb") as buf:
                shutil.copyfileobj(file.file, buf)

        # ── Direct image URL → synthetic 1-row CSV ────────────────────────
        elif url and url.startswith("http"):
            job_id    = f"direct_{str(uuid.uuid4())[:8]}"
            file_path = temp_dir / f"{job_id}_direct.csv"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"Category,Image URL\n{category},{url}\n")

        else:
            raise HTTPException(status_code=400, detail="Invalid file or URL provided.")

        # ── Queue background task ──────────────────────────────────────────
        background_tasks.add_task(
            process_excel_background, job_id, str(file_path), category
        )

        return {
            "status":  "success",
            "job_id":  job_id,
            "message": "Bulk generation started!",
        }

    except HTTPException:
        raise
    except Exception as exc:
        print(f"[bulk-generate] Server Error: {exc}")
        raise HTTPException(status_code=500, detail="Internal server error occurred.")


# ── Poll job status ────────────────────────────────────────────────────────────

@router.get("/bulk-status/{job_id}")
async def check_bulk_status(job_id: str):
    """
    Poll the status of a running bulk job.

    Returns:
    - **status**: "processing" | "completed" | "failed"
    - **progress**: Human-readable progress string
    - **results**: List of processed product results so far
    - **error**: Error message if status is "failed"
    """
    status = get_job_status(job_id)
    if not status:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found.")
    return status
