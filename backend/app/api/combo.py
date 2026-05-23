"""
Router: /api/combo-generate
Handles multi-piece jewelry combo flows.

Preset Flows:
  Flow 1 — "Bridal Trio":   ring + earring + necklace
  Flow 2 — "Classic Set":   necklace + bracelet + earring

Each piece requires its own reference image upload.
All pieces are generated in parallel; results are returned grouped by piece.
"""
import uuid
import asyncio

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from typing import Optional
from app.services.generator import generate_shots

router = APIRouter(prefix="/api", tags=["Combo"])

# ── Predefined combo flows ────────────────────────────────────────────────────

COMBO_FLOWS = {
    "bridal_trio": {
        "label": "Bridal Trio",
        "description": "Ring · Earring · Necklace",
        "pieces": ["ring", "earring", "necklace"],
        "emoji":  ["💍", "✨", "📿"],
    },
    "classic_set": {
        "label": "Classic Set",
        "description": "Necklace · Bracelet · Earring",
        "pieces": ["necklace", "bracelet", "earring"],
        "emoji":  ["📿", "💎", "✨"],
    },
}


@router.get("/combo-flows")
async def get_combo_flows():
    """Return all available combo flow presets."""
    return {"flows": COMBO_FLOWS}


@router.post("/combo-generate")
async def combo_generate(
    flow_id:    str           = Form(...),
    product_id: Optional[str] = Form(None),
    # Up to 3 files (one per piece in the flow)
    file_0:     Optional[UploadFile] = File(None),
    file_1:     Optional[UploadFile] = File(None),
    file_2:     Optional[UploadFile] = File(None),
):
    """
    Generate all jewelry pieces in a combo flow simultaneously.

    - **flow_id**:     One of 'bridal_trio' or 'classic_set'
    - **product_id**:  Optional session/folder name prefix
    - **file_0/1/2**: Reference images for each piece (in flow order)
    """
    if flow_id not in COMBO_FLOWS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown combo flow '{flow_id}'. Valid options: {list(COMBO_FLOWS.keys())}",
        )

    flow = COMBO_FLOWS[flow_id]
    pieces = flow["pieces"]  # e.g. ["ring", "earring", "necklace"]
    uploaded_files = [file_0, file_1, file_2]

    # Validate: all required files must be present
    for i, category in enumerate(pieces):
        f = uploaded_files[i]
        if not f or not getattr(f, "filename", None):
            raise HTTPException(
                status_code=400,
                detail=f"Missing image for piece {i + 1}: '{category}'. "
                       f"Please upload a reference photo for every item in the flow.",
            )

    # Build session prefix
    prefix = (product_id or "").strip() or f"combo-{str(uuid.uuid4())[:8]}"
    combo_session_id = prefix  # top-level session used for ZIP download

    async def _generate_piece(index: int, category: str) -> dict:
        """Read file and generate shots for a single piece."""
        f = uploaded_files[index]
        contents = await f.read()
        mime_type = f.content_type or "image/jpeg"
        if not mime_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail=f"File for '{category}' is not a valid image.",
            )

        # Each piece gets its own sub-folder inside the combo session
        piece_session_id = f"{prefix}/{category}"

        results = await generate_shots(
            image_bytes=contents,
            mime_type=mime_type,
            category_raw=category,
            session_id=piece_session_id,
            requested_shots=None,
            mode="standard",
        )
        return {
            "category":   category,
            "session_id": piece_session_id,
            "images":     results,
        }

    try:
        # Run all pieces in parallel
        piece_results = await asyncio.gather(*[
            _generate_piece(i, cat)
            for i, cat in enumerate(pieces)
        ])

        return {
            "status":     "success",
            "flow_id":    flow_id,
            "flow_label": flow["label"],
            "session_id": combo_session_id,
            "pieces":     list(piece_results),
        }

    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        print(f"[combo] Server Error: {exc}")
        raise HTTPException(status_code=500, detail="Internal server error during combo generation.")
