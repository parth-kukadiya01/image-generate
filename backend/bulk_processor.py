import asyncio
import uuid
import pandas as pd
import aiohttp
import mimetypes
from pathlib import Path
from generator import generate_shots, generate_shots_from_text

# In-memory storage for jobs
# Format: { "job_id": { "status": "processing", "progress": "0/10", "results": [] } }
jobs = {}

async def download_image(url: str) -> tuple[bytes, str]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise ValueError(f"Failed to download image from {url}")
            
            content_type = response.headers.get('Content-Type', '')
            if not content_type.startswith('image/'):
                content_type = mimetypes.guess_type(url)[0] or 'image/jpeg'
                
            contents = await response.read()
            return contents, content_type

async def process_excel_background(job_id: str, file_path: str, global_category: str):
    jobs[job_id] = {"status": "processing", "progress": "Initializing...", "results": []}
    
    try:
        # Read Excel or CSV
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        
        # Determine URL or Prompt column
        url_col = None
        prompt_col = None
        for col in df.columns:
            if 'url' in col.lower() or 'image url' in col.lower() or 'link' in col.lower():
                url_col = col
                break
            elif 'image prompt' in col.lower() or 'prompt' in col.lower():
                prompt_col = col

        if not url_col and not prompt_col:
            raise ValueError("No column found containing 'image url', 'image prompt', 'url', 'image', or 'link'.")

        total_rows = len(df)
        
        for index, row in df.iterrows():
            row_num = index + 1
            jobs[job_id]["progress"] = f"Processing row {row_num}/{total_rows}..."
            
            # Use specific category from row if provided, else use global_category
            category_col = next((c for c in df.columns if 'category' in c.lower() or 'piece type' in c.lower()), None)
            category = str(row[category_col]) if category_col and pd.notna(row[category_col]) else global_category
            
            try:
                session_id = f"bulk_{job_id}_{row_num}"
                
                if url_col and pd.notna(row[url_col]) and str(row[url_col]).startswith('http'):
                    image_url = str(row[url_col])
                    contents, mime_type = await download_image(image_url)
                    results = await generate_shots(
                        image_bytes=contents,
                        mime_type=mime_type,
                        category_raw=category,
                        session_id=session_id
                    )
                    identifier = image_url
                elif prompt_col and pd.notna(row[prompt_col]):
                    text_prompt = str(row[prompt_col])
                    results = await generate_shots_from_text(
                        prompt_text=text_prompt,
                        category_raw=category,
                        session_id=session_id
                    )
                    identifier = text_prompt[:30] + "..."
                else:
                    raise ValueError("No valid prompt or URL found for this row.")
                
                jobs[job_id]["results"].append({
                    "row": row_num,
                    "url": identifier,
                    "category": category,
                    "success": True,
                    "shots": results
                })
                
            except Exception as e:
                print(f"Error on row {row_num}: {e}")
                jobs[job_id]["results"].append({
                    "row": row_num,
                    "url": f"Row {row_num}",
                    "category": category,
                    "success": False,
                    "error": str(e)
                })

        jobs[job_id]["status"] = "completed"
        jobs[job_id]["progress"] = f"Completed {total_rows}/{total_rows}"
    
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)

def get_job_status(job_id: str):
    return jobs.get(job_id)
