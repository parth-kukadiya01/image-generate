"""
Router: /api/categories
Returns all available jewelry categories and social/creative scenes
for the frontend to build its configuration UI.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["Categories"])


@router.get("/categories")
async def get_categories():
    """Return the available categories and their shots for the frontend to build a UI."""
    from app.services.generator import CATEGORIES, CREATIVE_SCENES

    frontend_categories = {}
    for cat_name, cat_data in CATEGORIES.items():
        frontend_categories[cat_name] = {
            "worn_on": cat_data["worn_on"],
            "product": [{"key": s["key"], "label": s["label"]} for s in cat_data.get("product", [])],
            "model":   [{"key": s["key"], "label": s["label"]} for s in cat_data.get("model",   [])],
        }

    social_scenes = [{"key": s["key"], "label": s["label"]} for s in CREATIVE_SCENES]

    return {
        "categories":    frontend_categories,
        "social_scenes": social_scenes,
    }
