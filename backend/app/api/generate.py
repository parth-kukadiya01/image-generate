"""
Router: /api/generate
Handles single-image jewelry generation (Studio Mode & Creative/Social Mode).
Accepts either an uploaded file or a direct image URL.
"""
import uuid
import aiohttp

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from app.services.generator import generate_shots

router = APIRouter(prefix="/api", tags=["Generate"])


# ── Helpers ────────────────────────────────────────────────────────────────────

async def _download_image_bytes(url: str) -> tuple[bytes, str]:
    """Download an image from a URL and return (bytes, mime_type)."""
    import mimetypes

    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
            if resp.status != 200:
                raise HTTPException(
                    status_code=400,
                    detail=f"Could not download image from URL (HTTP {resp.status}).",
                )
            content_type = resp.headers.get("Content-Type", "")

            if "text/html" in content_type:
                raise HTTPException(
                    status_code=400,
                    detail="The URL points to a webpage, not a direct image file.",
                )

            contents = await resp.read()

            if contents.startswith(b"<html") or contents.startswith(b"<!DOCTYPE") or contents.startswith(b"<HTML"):
                raise HTTPException(
                    status_code=400,
                    detail="The URL returned an HTML webpage instead of an image.",
                )

            if not content_type.startswith("image/"):
                content_type = mimetypes.guess_type(url)[0] or "image/jpeg"

            return contents, content_type


# ── Endpoint ──────────────────────────────────────────────────────────────────

@router.post("/generate")
async def generate_jewelry_images(
    category:       str            = Form(...),
    product_id:     str | None     = Form(None),
    file:           UploadFile | None = File(None),
    image_url:      str | None     = Form(None),
    selected_shots: str | None     = Form(None),
    mode:           str            = Form("standard"),
):
    """
    Generate jewelry images for a single product.

    - **category**:       Jewelry type (ring, necklace, bracelet, …)
    - **product_id**:     Optional folder/product identifier
    - **file**:           Reference image upload (multipart)
    - **image_url**:      Direct URL to a reference image (alternative to file)
    - **selected_shots**: Comma-separated shot keys to force specific angles
    - **mode**:           "standard" | "social"  (social = creative scenes)
    """
    try:
        # ── Parse selected shots ───────────────────────────────────────────
        requested_shots = None
        if selected_shots and selected_shots.strip():
            requested_shots = [s.strip() for s in selected_shots.split(",") if s.strip()]

        # ── Resolve image bytes ────────────────────────────────────────────
        if file and getattr(file, "filename", None):
            contents  = await file.read()
            mime_type = file.content_type or "image/jpeg"
            if not mime_type.startswith("image/"):
                raise HTTPException(status_code=400, detail="Uploaded file must be an image.")
        elif image_url and image_url.strip():
            contents, mime_type = await _download_image_bytes(image_url.strip())
        else:
            raise HTTPException(
                status_code=400,
                detail="Please upload an image file or provide an image URL.",
            )

        # ── Resolve product / session ID ───────────────────────────────────
        pid = (product_id or "").strip() or f"gen-{str(uuid.uuid4())[:8]}"

        # ── Generate ───────────────────────────────────────────────────────
        results = await generate_shots(
            image_bytes=contents,
            mime_type=mime_type,
            category_raw=category,
            session_id=pid,
            requested_shots=requested_shots,
            mode=mode,
        )

        return {"status": "success", "product_id": pid, "session_id": pid, "images": results}

    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        print(f"[generate] Server Error: {exc}")
        raise HTTPException(status_code=500, detail="Internal server error during generation.")
