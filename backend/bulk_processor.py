import asyncio
import json
import uuid
import pandas as pd
import aiohttp
import mimetypes
from datetime import datetime
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
            if "text/html" in content_type:
                raise ValueError(f"The URL points to a webpage, not a direct image file: {url}")
                
            contents = await response.read()
            
            if contents.startswith(b'<html') or contents.startswith(b'<!DOCTYPE') or contents.startswith(b'<HTML'):
                raise ValueError(f"The URL returned an HTML webpage instead of an image: {url}")

            if not content_type.startswith('image/'):
                content_type = mimetypes.guess_type(url)[0] or 'image/jpeg'
                
            return contents, content_type

def write_row_log(out_dir: Path, product_id: str, category: str, row_num: int,
                  shot_results: list[dict], timestamp: str) -> None:
    """Write generation_log.json inside each product's output folder."""
    out_dir.mkdir(parents=True, exist_ok=True)
    
    success_count = sum(1 for r in shot_results if r.get("url"))
    failed_count  = len(shot_results) - success_count

    log_data = {
        "product_id": product_id,
        "category":   category,
        "row":        row_num,
        "timestamp":  timestamp,
        "total":      len(shot_results),
        "success":    success_count,
        "failed":     failed_count,
        "shots":      shot_results,
    }
    try:
        (out_dir / "generation_log.json").write_text(
            json.dumps(log_data, indent=2), encoding="utf-8"
        )
    except Exception as e:
        print(f"Could not write log for {product_id}: {e}")

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
        product_id_col = None
        
        for col in df.columns:
            col_lower = col.strip().lower()
            if col_lower in ('product_id', 'product id', 'productid', 'id', 'sku'):
                product_id_col = col
            elif 'url' in col_lower or 'image url' in col_lower or 'link' in col_lower:
                url_col = col
            elif 'image prompt' in col_lower or 'prompt' in col_lower:
                prompt_col = col

        if not url_col and not prompt_col:
            raise ValueError("No column found containing 'image url', 'image prompt', 'url', 'image', or 'link'.")

        total_rows = len(df)
        
        for index, row in df.iterrows():
            row_num = index + 1
            if index < 15:
                continue
            jobs[job_id]["progress"] = f"Processing row {row_num}/{total_rows}..."
            
            # Use specific category from row if provided, else use global_category
            category_col = next((c for c in df.columns if 'category' in c.lower() or 'piece type' in c.lower()), None)
            category = str(row[category_col]).strip().lower() if category_col and pd.notna(row[category_col]) else global_category
            
            # Resolve product_id
            if product_id_col and pd.notna(row[product_id_col]) and str(row[product_id_col]).strip():
                product_id = str(row[product_id_col]).strip()
            else:
                # Fallback: just row-{row_num} (no extra category prefix)
                product_id = f"row-{row_num}"
                
            try:
                # ── Resume logic: Skip if folder exists and has images ──
                out_dir = Path("outputs") / product_id
                if out_dir.exists():
                    existing_images = list(out_dir.glob("*.jpg")) + list(out_dir.glob("*.png"))
                    if len(existing_images) >= 6: # Assuming we expect 6 shots
                        print(f"Skipping row {row_num}: {product_id} already exists with {len(existing_images)} images.")
                        # Load existing results for the status UI
                        results = []
                        for img in existing_images:
                            results.append({"url": f"/outputs/{product_id}/{img.name}", "label": img.stem.replace("_", " ").title()})
                        
                        jobs[job_id]["results"].append({
                            "row": row_num,
                            "product_id": product_id,
                            "url": "Skipped (Existing)",
                            "category": category,
                            "success": True,
                            "shots": results
                        })
                        continue

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                if url_col and pd.notna(row[url_col]) and str(row[url_col]).startswith('http'):
                    image_url = str(row[url_col])
                    contents, mime_type = await download_image(image_url)
                    results = await generate_shots(
                        image_bytes=contents,
                        mime_type=mime_type,
                        category_raw=category,
                        session_id=product_id
                    )
                    identifier = image_url
                elif prompt_col and pd.notna(row[prompt_col]):
                    text_prompt = str(row[prompt_col])
                    results = await generate_shots_from_text(
                        prompt_text=text_prompt,
                        category_raw=category,
                        session_id=product_id
                    )
                    identifier = text_prompt[:30] + "..."
                else:
                    raise ValueError("No valid prompt or URL found for this row.")
                
                # Write log inside the product folder
                out_dir = Path("outputs") / product_id
                write_row_log(out_dir, product_id, category, row_num, results, timestamp)
                
                jobs[job_id]["results"].append({
                    "row": row_num,
                    "product_id": product_id,
                    "url": identifier,
                    "category": category,
                    "success": True,
                    "shots": results
                })
                
            except Exception as e:
                print(f"Error on row {row_num}: {e}")
                jobs[job_id]["results"].append({
                    "row": row_num,
                    "product_id": product_id,
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
