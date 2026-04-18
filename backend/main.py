from fastapi import FastAPI, UploadFile, Form, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uuid
import os
import shutil
import aiohttp
from pathlib import Path

import urllib.request
import re
from generator import generate_shots
from bulk_processor import process_excel_background, get_job_status

app = FastAPI(title="Jewelry Image Generator API")

# Allow CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure outputs directory exists
outputs_dir = Path("outputs")
outputs_dir.mkdir(exist_ok=True)

# Mount outputs directory so frontend can fetch images
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

async def download_image_bytes(url: str) -> tuple[bytes, str]:
    """Download an image from a URL and return (bytes, mime_type)."""
    import mimetypes
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
            if resp.status != 200:
                raise HTTPException(status_code=400, detail=f"Could not download image from URL (HTTP {resp.status}).")
            content_type = resp.headers.get("Content-Type", "")
            if "text/html" in content_type:
                raise HTTPException(status_code=400, detail="The URL points to a webpage, not a direct image file.")
                
            contents = await resp.read()
            
            if contents.startswith(b'<html') or contents.startswith(b'<!DOCTYPE') or contents.startswith(b'<HTML'):
                raise HTTPException(status_code=400, detail="The URL returned an HTML webpage instead of an image.")

            if not content_type.startswith("image/"):
                content_type = mimetypes.guess_type(url)[0] or "image/jpeg"
                
            return contents, content_type


@app.post("/api/generate")
async def generate_jewelry_images(
    category: str = Form(...),
    product_id: str | None = Form(None),
    file: UploadFile | None = File(None),
    image_url: str | None = Form(None),
):
    try:
        # ── Resolve image bytes ───────────────────────────────────────────────
        if file and getattr(file, "filename", None):
            contents = await file.read()
            mime_type = file.content_type or "image/jpeg"
            if not mime_type.startswith("image/"):
                raise HTTPException(status_code=400, detail="Uploaded file must be an image.")
        elif image_url and image_url.strip():
            contents, mime_type = await download_image_bytes(image_url.strip())
        else:
            raise HTTPException(status_code=400, detail="Please upload an image file or provide an image URL.")

        # ── Resolve folder name / product ID ─────────────────────────────────
        pid = product_id.strip() if product_id else ""
        if not pid:
            # Fallback for missing product_id: clean short ID
            pid = f"gen-{str(uuid.uuid4())[:8]}"

        # Generate images — folder = product ID
        results = await generate_shots(
            image_bytes=contents,
            mime_type=mime_type,
            category_raw=category,
            session_id=pid
        )

        return {"status": "success", "product_id": pid, "session_id": pid, "images": results}
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Server Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error occurred during generation.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

@app.post("/api/bulk-generate")
async def start_bulk_generation(
    background_tasks: BackgroundTasks,
    category: str = Form(...),
    file: UploadFile | None = File(None),
    url: str | None = Form(None)
):
    try:
        if not file and not url:
            raise HTTPException(status_code=400, detail="Must provide an Excel file or a Google Sheets URL.")
            
        temp_dir = Path("outputs") / "temp_excel"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        if url and "docs.google.com/spreadsheets" in url:
            # Handle Google Sheets URL
            match = re.search(r'/d/([a-zA-Z0-9-_]+)', url)
            if not match:
                raise HTTPException(status_code=400, detail="Could not extract document ID from URL.")
                
            doc_id = match.group(1)
            job_id = doc_id
            csv_export_url = f"https://docs.google.com/spreadsheets/d/{doc_id}/export?format=csv"
            
            # Save as {job_id}_sheet.csv as per requirements
            file_path = temp_dir / f"{job_id}_sheet.csv"
            
            # Skip downloading if the file already exists
            if not file_path.exists():
                urllib.request.urlretrieve(csv_export_url, file_path)
            
        elif file:
            # Validate Excel file
            if not file.filename.endswith(('.xlsx', '.xls', '.csv')):
                raise HTTPException(status_code=400, detail="Uploaded file must be an Excel or CSV file.")
    
            # Sanitize filename for job_id (no extension)
            base_filename = os.path.splitext(file.filename)[0]
            job_id = "".join(c for c in base_filename if c.isalnum() or c in (' ', '_', '-')).replace(" ", "_").lower()
            
            # Ensure folder name is clean
            safe_filename = "".join(c for c in file.filename if c.isalnum() or c in ('.', '_', '-'))
            file_path = temp_dir / safe_filename
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
                
        elif url and url.startswith("http"):
            # They passed a direct image URL, create a dummy 1-row CSV for the bulk processor
            job_id = f"direct_{str(uuid.uuid4())[:8]}"
            file_path = temp_dir / f"{job_id}_direct.csv"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"Category,Image URL\n{category},{url}\n")
                
        else:
            raise HTTPException(status_code=400, detail="Invalid file or URL provided.")

        # Start background processing
        background_tasks.add_task(process_excel_background, job_id, str(file_path), category)

        return {"status": "success", "job_id": job_id, "message": "Bulk generation started!"}
        
    except Exception as e:
        print(f"Server Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error occurred.")

@app.get("/api/bulk-status/{job_id}")
async def check_bulk_status(job_id: str):
    status = get_job_status(job_id)
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    return status
