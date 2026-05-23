"""
Router: /api/download-zip/{session_id}
Streams all generated images for a session as a single ZIP file.
Also supports /api/download-zip-bulk/{job_id} to zip an entire bulk job.
"""
import io
import zipfile
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/api", tags=["Download"])

OUTPUTS_DIR = Path("outputs")


def _zip_folder(folder: Path, zip_name: str) -> StreamingResponse:
    """Zip all images in *folder* and return as a streaming response."""
    image_files = sorted(
        [f for f in folder.iterdir() if f.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp")]
    )

    if not image_files:
        raise HTTPException(status_code=404, detail="No images found for this session.")

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for img_path in image_files:
            zf.write(img_path, arcname=img_path.name)
    buf.seek(0)

    return StreamingResponse(
        buf,
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{zip_name}.zip"'},
    )


# ── Single-session ZIP ────────────────────────────────────────────────────────

@router.get("/download-zip/{session_id}")
async def download_session_zip(session_id: str):
    """
    Download all generated images for a single session as a ZIP file.
    session_id is the product_id / folder name under outputs/.
    """
    folder = OUTPUTS_DIR / session_id
    if not folder.exists() or not folder.is_dir():
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found.")

    return _zip_folder(folder, zip_name=session_id)


# ── Bulk-job ZIP (entire job, all products) ───────────────────────────────────

@router.get("/download-zip-bulk/{job_id}")
async def download_bulk_zip(job_id: str):
    """
    Download ALL images from ALL products in a bulk job as one ZIP.
    The archive preserves the per-product sub-folder structure.
    """
    from app.services.bulk_processor import get_job_status

    job = get_job_status(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found.")
    if job["status"] not in ("completed", "processing"):
        raise HTTPException(status_code=400, detail="Job has not produced any results yet.")

    product_ids = [r["product_id"] for r in (job.get("results") or []) if r.get("success")]
    if not product_ids:
        raise HTTPException(status_code=404, detail="No successful products found in this job.")

    buf = io.BytesIO()
    total = 0
    with zipfile.ZipFile(buf, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for pid in product_ids:
            folder = OUTPUTS_DIR / pid
            if not folder.exists():
                continue
            for img_path in sorted(folder.iterdir()):
                if img_path.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"):
                    zf.write(img_path, arcname=f"{pid}/{img_path.name}")
                    total += 1

    if total == 0:
        raise HTTPException(status_code=404, detail="No images found for this bulk job.")

    buf.seek(0)
    return StreamingResponse(
        buf,
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="bulk_{job_id}.zip"'},
    )
