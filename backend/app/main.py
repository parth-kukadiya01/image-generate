"""
Jewelry Image Generator — FastAPI application entry-point.

All business-logic endpoints live in app/api/:
  • app/api/categories.py  →  GET  /api/categories
  • app/api/generate.py    →  POST /api/generate
  • app/api/bulk.py        →  POST /api/bulk-generate
                               GET  /api/bulk-status/{job_id}
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# ── Import routers ─────────────────────────────────────────────────────────────
from app.api.categories import router as categories_router
from app.api.generate    import router as generate_router
from app.api.bulk        import router as bulk_router
from app.api.download    import router as download_router
from app.api.combo       import router as combo_router

# ── App setup ─────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Jewelry Image Generator API",
    description=(
        "AI-powered jewelry photography generation engine. "
        "Supports single-product studio shots, social/creative editorial modes, "
        "and bulk Excel/Google-Sheets batch processing."
    ),
    version="2.0.0",
)

# ── CORS (allow all origins for local dev) ────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Static files: serve generated images ──────────────────────────────────────
outputs_dir = Path("outputs")
outputs_dir.mkdir(exist_ok=True)
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

# ── Register routers ──────────────────────────────────────────────────────────
app.include_router(categories_router)
app.include_router(generate_router)
app.include_router(bulk_router)
app.include_router(download_router)
app.include_router(combo_router)


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["System"])
async def health():
    """Quick liveness probe."""
    return {"status": "ok", "version": "2.0.0"}


# ── Dev runner ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
