from fastapi import FastAPI, UploadFile, Form, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uuid
import os
import shutil
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

@app.post("/api/generate")
async def generate_jewelry_images(
    category: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        # Read uploaded image
        contents = await file.read()
        mime_type = file.content_type
        
        if not mime_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Uploaded file must be an image.")

        # Create unique session ID
        session_id = str(uuid.uuid4())

        # Generate images using the provided logic
        results = await generate_shots(
            image_bytes=contents,
            mime_type=mime_type,
            category_raw=category,
            session_id=session_id
        )

        return {"status": "success", "session_id": session_id, "images": results}
        
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
            
        job_id = str(uuid.uuid4())
        
        temp_dir = Path("outputs") / "temp_excel"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        if url and "docs.google.com/spreadsheets" in url:
            # Handle Google Sheets URL
            match = re.search(r'/d/([a-zA-Z0-9-_]+)', url)
            if not match:
                raise HTTPException(status_code=400, detail="Could not extract document ID from URL.")
                
            doc_id = match.group(1)
            csv_export_url = f"https://docs.google.com/spreadsheets/d/{doc_id}/export?format=csv"
            
            file_path = temp_dir / f"{job_id}_sheet.csv"
            urllib.request.urlretrieve(csv_export_url, file_path)
            
        elif file:
            # Validate Excel file
            if not file.filename.endswith(('.xlsx', '.xls', '.csv')):
                raise HTTPException(status_code=400, detail="Uploaded file must be an Excel or CSV file.")
    
            # Save Excel file temporarily
            file_path = temp_dir / f"{job_id}_{file.filename}"
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
                
        elif url and url.startswith("http"):
            # They passed a direct image URL, create a dummy 1-row CSV for the bulk processor
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
