"""
config.py
─────────
Central configuration for the Jewelry Image Generator.
All tuneable knobs live here — change once, applied everywhere.
"""

# ── Gemini API ─────────────────────────────────────────────────────────────
GEMINI_API_KEY = "AIzaSyDLuOQ14kNc_dA8v9oBZYkdohPfXYlN3cQ"
MODEL          = "gemini-2.5-flash-image"   # image-capable model

# ── Shot counts ────────────────────────────────────────────────────────────
TOTAL_PRODUCT = 4   # product-only shots per run
TOTAL_MODEL   = 0   # model/lifestyle shots per run

# ── Branding ───────────────────────────────────────────────────────────────
LOGO_PATH = "/Users/parthkukadiya/work/pint_automation/riolls_logo.png"
