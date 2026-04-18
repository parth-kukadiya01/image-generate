import os
import asyncio
import mimetypes
import random
from pathlib import Path
from PIL import Image
from google import genai
from google.genai import types

GEMINI_API_KEY = "AIzaSyBRYRW4UxifNDI65wArxv0wWbDcACXWuyI"
MODEL          = "gemini-2.5-flash-image" # Correcting to the intended model if approved
TOTAL_PRODUCT  = 4
TOTAL_MODEL    = 0
LOGO_PATH      = "/Users/parthkukadiya/work/pint_automation/riolls_logo.png"

# BRAND THEME CONSISTENCY
GLOBAL_THEME_RULES = """
BRAND VISUAL IDENTITY (THEME):
- BACKGROUND: Use a high-end, textured "Creamy Marble" or luxury natural light stone surface for all product shots.
- LIGHTING: Soft, directional natural side-window lighting that creates elegant shadows and emphasizes metal texture.
- AESTHETIC: Quiet luxury, minimalist, and sophisticated.
- DO NOT use different backgrounds or inconsistent lighting across shots.
"""


CATEGORIES = {
    # ── RING ──────────────────────────────────────────────────────────────────
    "ring": {
        "worn_on": "ring finger",
        "product": [
            {
                "key":   "01_product_front",
                "label": "Product — Straight Front",
                "shot":  (
                    "The ring standing upright on a textured, creamy marble surface, shot straight-on "
                    "from the front at eye level. The face of the ring fills the frame symmetrically. "
                    "Soft window light from the side, creating organic shadows. Elegant hero product shot."
                ),
            },
            {
                "key":   "03_product_top_down",
                "label": "Product — Top-Down",
                "shot":  (
                    "The ring lying flat on a luxury natural stone surface, shot from directly above (top-down bird's-eye view). "
                    "Full face of the center stone, halo, and band fully visible. "
                    "Perfect symmetry. Soft overhead natural lighting, shallow depth of field."
                ),
            },
            {
                "key":   "08_product_laying_glamour",
                "label": "Product — Laying Angle",
                "shot":  (
                    "The ring laying on its side at a dynamic 45-degree angle on a creamy marble surface. "
                    "Shows the entire band and the face tilted elegantly toward the lens. "
                    "Soft natural highlights, organic shadows, professional jewelry photography."
                ),
            },
            {
                "key":   "09_product_three_quarter_profile",
                "label": "Product — 3/4 Perspective",
                "shot":  (
                    "The ring standing on a textured natural stone surface, shot from a 45-degree three-quarter profile. "
                    "Shows the side of the band and the face of the stone simultaneously. "
                    "Dramatic natural side lighting, realistic depth of field."
                ),
            },
        ],
        "model": [
            {
                "key":   "05_model_hand_front",
                "label": "Model — Hand Front",
                "shot":  (
                    "A real female hand with natural skin texture, visible pores, and neat nude-polished nails. "
                    "The ring sits on the ring finger at its REAL, natural size. "
                    "Hand raised gracefully, shot straight-on. "
                    "Soft natural light from a window, shallow depth of field. "
                    "Indistinguishable from a genuine luxury jewelry editorial."
                ),
            },
            {
                "key": "06_model_hand_glamour",
                "label": "Model — Hand Glamour",
                "shot": (
                    "A high-end luxury jewelry editorial photograph of a real female hand with "
                    "flawless natural skin texture and organic warmth. "
                    "The hand is held at a graceful 45-degree angle. The ring is worn at its "
                    "perfect, realistic scale — never oversized. "
                    "The lighting is soft-box quality combined with natural ambient light. "
                    "The background is a creamy neutral bokeh. Real proportions and skin details."
                ),
            },
            {
                "key": "12_model_index_finger",
                "label": "Model — Index Finger Close-Up",
                "shot": (
                    "A close-up of a real woman's index finger wearing the ring. "
                    "Shows the ring from a slightly side-angled view. "
                    "Natural window lighting, sharp skin details, soft-focus palm/background."
                ),
            },
            {
                "key": "13_model_hand_lifestyle",
                "label": "Model — Hand Lifestyle Pose",
                "shot": (
                    "A real woman's hand resting naturally on the lapel of a wool blazer, wearing the ring. "
                    "Natural daylight, realistic skin and fabric texture. "
                    "High-end lifestyle photography, authentic luxury vibe."
                ),
            },
        ],
    },

    # ── NECKLACE ──────────────────────────────────────────────────────────────
    "necklace": {
        "worn_on": "neck and collarbone",
        "product": [
            {
                "key":   "01_product_hanging",
                "label": "Product — Hanging Front",
                "shot":  (
                    "The necklace hanging vertically, shot straight-on against a creamy marble surface. "
                    "Chain drapes naturally. Soft directional lighting creating subtle depth. "
                    "Classic, realistic luxury product photography."
                ),
            },
            {
                "key":   "02_product_flat_lay",
                "label": "Product — Flat Lay",
                "shot":  (
                    "The necklace laid flat on a luxury natural stone surface, shot top-down. "
                    "Chain arranged in a clean arc. Natural window lighting catching the stone facets. "
                    "Shows full length and pendant detail with organic shadows."
                ),
            },
            {
                "key":   "03_product_pendant_close",
                "label": "Product — Pendant Close-Up",
                "shot":  (
                    "Close-up of the pendant only, on a creamy marble surface. "
                    "Fills most of the frame. All facets and metal details razor-sharp. "
                    "Dramatic side lighting, extremadamente shallow depth of field."
                ),
            },
            {
                "key":   "04_product_glamour",
                "label": "Product — Glamour 45°",
                "shot":  (
                    "The necklace hanging, shot from a 45-degree glamour angle slightly elevated against a natural stone surface. "
                    "Soft bokeh background, natural light source, pendant depth clearly visible."
                ),
            },
        ],
        "model": [
            {
                "key": "05_model_neck_front",
                "label": "Model — Neck Front",
                "shot": (
                    "A high-end editorial jewelry portrait of a real woman wearing the necklace, "
                    "framing the collarbone and neck. The necklace rests naturally on her bare skin "
                    "at its true, real-world scale (pendant approx. 15-30mm). "
                    "Soft natural lighting highlights the skin's natural texture and pores. "
                    "Minimalist, slightly out-of-focus background. Raw photography style."
                ),
            },
            {
                "key": "06_model_pendant_macro",
                "label": "Model — Pendant Close-Up",
                "shot": (
                    "An extreme macro close-up of the pendant resting on a real woman's collarbone. "
                    "Lighting is warm and natural. Extremely shallow depth of field: "
                    "the pendant is in razor-sharp focus while the skin texture and surroundings "
                    "softly blur. Authentic luxury editorial look."
                ),
            },
            {
                "key":   "09_model_clothing_lifestyle",
                "label": "Model — Over Clothing Lifestyle",
                "shot":  (
                    "A real woman wearing a silky neutral-toned blouse, with the necklace resting elegantly. "
                    "Realistic scales. Natural window lighting, soft shadows on the fabric. "
                    "High-end lifestyle photography vibe."
                ),
            },
            {
                "key":   "12_model_neck_side_profile",
                "label": "Model — Neck Side Angle",
                "shot":  (
                    "A real woman shot from a side profile, wearing the necklace. "
                    "Shows how the chain wraps the neck and the pendant hangs. "
                    "Natural window light, shallow depth of field, sharp skin detail."
                ),
            },
        ],
    },

    # ── BRACELET ──────────────────────────────────────────────────────────────
    "bracelet": {
        "worn_on": "wrist",
        "product": [
            {
                "key":   "01_product_front",
                "label": "Product — Front Upright",
                "shot":  (
                    "The bracelet standing upright on a textured creamy marble surface, shot straight-on. "
                    "Soft natural lighting, organic shadows, clean and realistic presentation."
                ),
            },
            {
                "key":   "02_product_glamour",
                "label": "Product — Glamour 45°",
                "shot":  (
                    "The bracelet at a 45-degree angle on a luxury natural stone surface. "
                    "Shows the front face and side depth. Dramatic side lighting, "
                    "luxury jewelry advertisement style."
                ),
            },
            {
                "key":   "03_product_top_down",
                "label": "Product — Top-Down",
                "shot":  (
                    "The bracelet lying flat on a creamy marble surface, shot from directly above. "
                    "Soft natural light, shallow depth of field, real-world texture."
                ),
            },
            {
                "key":   "04_product_detail",
                "label": "Product — Clasp Detail",
                "shot":  (
                    "Close-up of the bracelet clasp on a natural stone surface. "
                    "Shows the craftsmanship and closure mechanism clearly. "
                    "Sharp focus, natural lighting."
                ),
            },
        ],
        "model": [
            {
                "key": "05_model_wrist_front",
                "label": "Model — Wrist Front",
                "shot": (
                    "A high-end commercial photograph of a real female wrist with "
                    "natural skin tone and texture (visible pores). The bracelet is worn naturally "
                    "at its correct, realistic size. Hand is relaxed. "
                    "Soft natural lighting illuminates the metal and stones. Photorealistic."
                ),
            },
            {
                "key": "06_model_wrist_lifestyle",
                "label": "Model — Wrist Lifestyle",
                "shot": (
                    "A lifestyle jewelry photograph featuring a real woman's wrist. "
                    "The hand rests naturally on a soft-textured surface. "
                    "Soft directional natural light creates subtle shadows. "
                    "Shallow depth of field, genuine proportions."
                ),
            },
            {
                "key": "09_model_wrist_clothing",
                "label": "Model — Over Cuff Sleeve",
                "shot": (
                    "The bracelet worn over the cuff of a high-end silk blouse. "
                    "Shows how it pairs with luxury fashion. Natural window light, "
                    "sharp focus on the jewelry, authentic fabric texture."
                ),
            },
        ],
    },

    # ── EARRING ───────────────────────────────────────────────────────────────
    "earring": {
        "worn_on": "earlobe",
        "product": [
            {
                "key":   "01_product_pair_front",
                "label": "Product — Pair Front",
                "shot":  (
                    "Both earrings as a matching pair, laid on a textured creamy marble surface side by side. "
                    "Soft natural lighting from the side, creating realistic depth and shadows. "
                    "Every detail sharp."
                ),
            },
            {
                "key":   "02_product_single_glamour",
                "label": "Product — Single Glamour",
                "shot":  (
                    "One single earring on a luxury natural stone pedestal, shot from a 45-degree angle. "
                    "Natural directional light catching the stones. Real-world texture."
                ),
            },
            {
                "key":   "03_product_top_down",
                "label": "Product — Pair Top-Down",
                "shot":  (
                    "Both earrings laid flat on a creamy marble surface, shot from directly above. "
                    "Symmetrically placed. Soft natural light, shallow depth of field."
                ),
            },
            {
                "key":   "04_product_side",
                "label": "Product — Single Side Profile",
                "shot":  (
                    "One single earring, shot from a 90-degree side profile on a natural stone surface. "
                    "Shows the depth and backing. Realistic lighting and shadows."
                ),
            },
        ],
        "model": [
            {
                "key": "05_model_ear_side",
                "label": "Model — Ear Side Profile",
                "shot": (
                    "A professional luxury jewelry photograph of a real woman's ear. "
                    "The earring is rendered at its precise natural size. "
                    "Lighting is crisp and natural, highlighting skin texture (pores, natural tones). "
                    "The earring is in razor-sharp focus against a soft-focus profile."
                ),
            },
            {
                "key": "06_model_ear_34",
                "label": "Model — Face 3/4 Angle",
                "shot": (
                    "A stunning three-quarter view portrait of a real woman. "
                    "The earring is in perfect proportion, appearing small and refined. "
                    "Soft natural window lighting, subtle bokeh. Photorealistic skin and hair."
                ),
            },
            {
                "key":   "09_model_windswept_action",
                "label": "Model — Lifestyle Action Hair",
                "shot":  (
                    "A woman's profile with her hand brushing hair behind her ear. "
                    "Earring catches natural light perfectly. Realistic skin and proportions. "
                    "Cinematic crop, lifestyle atmosphere."
                ),
            },
            {
                "key":   "12_model_ear_macro_skin",
                "label": "Model — Extreme Ear Macro",
                "shot":  (
                    "Extreme macro of the earring on a real woman's earlobe. "
                    "Razor-sharp focus on the stones, showing natural skin pores and texture. "
                    "Soft natural light, authentic luxury editorial."
                ),
            },
        ],
    },

    # ── PENDANT ───────────────────────────────────────────────────────────────
    "pendant": {
        "worn_on": "neck (on a chain)",
        "product": [
            {
                "key":   "01_product_front",
                "label": "Product — Pendant Front",
                "shot":  (
                    "The pendant alone on a piece of creamy marble, shot straight-on. "
                    "All details visible. Soft natural directional light, organic shadows."
                ),
            },
            {
                "key":   "02_product_glamour",
                "label": "Product — Pendant Glamour 45°",
                "shot":  (
                    "The pendant hanging on its chain against a luxury natural stone surface. "
                    "Shot from a 45-degree angle. Natural side lighting, professional product look."
                ),
            },
            {
                "key":   "03_product_top_down",
                "label": "Product — Top-Down",
                "shot":  (
                    "The pendant lying flat on a creamy marble surface, shot from directly above. "
                    "Natural morning light catching the metal polish. Sharp focus."
                ),
            },
            {
                "key":   "04_product_back",
                "label": "Product — Back Detail",
                "shot":  (
                    "The back of the pendant shown clearly on a natural stone surface. "
                    "Shows engravings and bail attachment. Realistic light, sharp focus."
                ),
            },
        ],
        "model": [
            {
                "key": "05_model_collarbone",
                "label": "Model — Pendant on Collarbone",
                "shot": (
                    "A high-end editorial jewelry portrait of a real woman wearing the pendant. "
                    "Pendant rests naturally at its true-to-life size (15-30mm). "
                    "Soft natural lighting highlights the skin's real texture. "
                    "Perfect focus on the piece."
                ),
            },
            {
                "key": "06_model_pendant_macro",
                "label": "Model — Pendant Macro Close-Up",
                "shot": (
                    "An exquisite macro photograph of the pendant on a real woman's skin. "
                    "Pendant is at its true, delicate scale. Natural lighting, catching stone facets. "
                    "Shallow depth of field, photorealistic luxury."
                ),
            },
            {
                "key": "09_model_lifestyle_holding",
                "label": "Model — Holding Pendant",
                "shot": (
                    "A real woman's hand gently touching or holding the pendant while wearing it. "
                    "Natural window light, realistic skin and nail texture. "
                    "Authentic, high-end lifestyle photography."
                ),
            },
        ],
    },

    # ── BANGLE ────────────────────────────────────────────────────────────────
    "bangle": {
        "worn_on": "wrist",
        "product": [
            {
                "key":   "01_product_upright",
                "label": "Product — Upright Front",
                "shot":  (
                    "The bangle standing upright on a textured creamy marble surface, shot straight-on. "
                    "Balanced natural light, organic shadows, clean and realistic."
                ),
            },
            {
                "key":   "03_product_glamour",
                "label": "Product — Glamour 45°",
                "shot":  (
                    "The bangle at a 45-degree angle on a luxury natural stone surface. "
                    "Shows stones and depth with dramatic side lighting."
                ),
            },
            {
                "key":   "02_product_top_down",
                "label": "Product — Top-Down",
                "shot":  (
                    "The bangle lying flat on a creamy marble surface, shot from above. "
                    "Natural window light, shallow depth of field, sharp focus on stones."
                ),
            },
            {
                "key":   "04_product_side",
                "label": "Product — Side Profile",
                "shot":  (
                    "The bangle standing upright on a natural stone surface, 90-degree side profile. "
                    "Shows width and stone arrangement. Realistic lighting."
                ),
            },
        ],
        "model": [
            {
                "key": "05_model_wrist_front",
                "label": "Model — Wrist Front",
                "shot": (
                    "A professional commercial shot of a real female wrist wearing the bangle at "
                    "its natural size. Soft natural lighting, clean background, "
                    "natural skin texture (pores visible). 100% photorealistic."
                ),
            },
            {
                "key": "06_model_wrist_lifestyle",
                "label": "Model — Wrist Lifestyle",
                "shot": (
                    "A relaxed, lifestyle jewelry photograph with the bangle on a real woman's wrist. "
                    "Natural light source, bokeh background, sharp focus on the bangle. "
                    "Real-person proportions."
                ),
            },
            {
                "key": "09_model_stacked_chic",
                "label": "Model — Stacked Style",
                "shot": (
                    "The bangle worn alongside a delicate watch or another thin bracelet. "
                    "Fashion-forward, luxury lifestyle look. Natural window light."
                ),
            },
        ],
    },

    # ── ANKLET ────────────────────────────────────────────────────────────────
    "anklet": {
        "worn_on": "ankle",
        "product": [
            {
                "key":   "01_product_flat_lay",
                "label": "Product — Flat Lay",
                "shot":  (
                    "The anklet laid flat on a creamy marble surface, shot top-down. "
                    "Natural window light, real-world shadows, sharp focus on detail."
                ),
            },
            {
                "key":   "02_product_glamour",
                "label": "Product — Glamour 45°",
                "shot":  (
                    "The anklet draped naturally at a 45-degree angle on a luxury natural stone surface. "
                    "Soft directional light, luxury jewelry photography atmosphere."
                ),
            },
            {
                "key":   "03_product_hanging",
                "label": "Product — Hanging Display",
                "shot":  (
                    "The anklet hanging vertically against a creamy marble surface. "
                    "Full length of chain visible. Natural lighting, realistic shadows."
                ),
            },
            {
                "key":   "04_product_charm_close",
                "label": "Product — Charm/Stone Close-Up",
                "shot":  (
                    "Close-up of any charms or stones on a natural stone surface. "
                    "Macro photography, extremadamente shallow depth of field, sharp focus."
                ),
            },
        ],
        "model": [
            {
                "key": "05_model_ankle_front",
                "label": "Model — Ankle Front",
                "shot": (
                    "A professional photograph of a real woman's ankle with the anklet "
                    "at its true natural size. Soft natural lighting, real skin textures. "
                    "Sharp focus on the jewelry."
                ),
            },
            {
                "key": "06_model_ankle_lifestyle",
                "label": "Model — Ankle Lifestyle",
                "shot": (
                    "A lifestyle photograph of a real woman's ankle on soft cotton fabric. "
                    "Natural warm light, shallow depth of field, authentic and photorealistic."
                ),
            },
            {
                "key": "09_model_sand_lifestyle",
                "label": "Model — Beach Lifestyle",
                "shot": (
                    "A real woman's ankle with the anklet, resting on natural sand. "
                    "Golden hour lighting, realistic skin and sand texture. "
                    "High-end vacation vibe."
                ),
            },
        ],
    },

    # ── BROOCH ────────────────────────────────────────────────────────────────
    "brooch": {
        "worn_on": "chest or lapel",
        "product": [
            {
                "key":   "01_product_front",
                "label": "Product — Front Hero",
                "shot":  (
                    "The brooch flat on a creamy marble surface, shot top-down. "
                    "All stones visible. Natural side lighting creating rich depth and shadows."
                ),
            },
            {
                "key":   "02_product_glamour",
                "label": "Product — Glamour 45°",
                "shot":  (
                    "The brooch propped on a luxury natural stone surface, shot from 45 degrees. "
                    "Dramatic natural lighting, luxury editorial style."
                ),
            },
            {
                "key":   "03_product_side",
                "label": "Product — Side Profile",
                "shot":  (
                    "The brooch shot from a 90-degree side profile on a creamy marble surface. "
                    "Shows pin mechanism. Realistic lighting, sharp focus."
                ),
            },
            {
                "key":   "04_product_stone_close",
                "label": "Product — Stone Close-Up",
                "shot":  (
                    "Extreme close-up of the brooch stones on a natural stone surface. "
                    "Macro studio lighting, extremadamente shallow depth of field, razor-sharp facets."
                ),
            },
        ],
        "model": [
            {
                "key": "05_model_lapel_front",
                "label": "Model — Lapel Front",
                "shot": (
                    "A sophisticated luxury jewelry photograph of a real woman wearing the "
                    "brooch on a wool blazer. Brooch is at true-to-life scale. "
                    "Professional natural lighting, realistic fabric and skin detail."
                ),
            },
            {
                "key": "06_model_lapel_close",
                "label": "Model — Lapel Close-Up",
                "shot": (
                    "An editorial close-up of the brooch on a real woman's lapel. "
                    "Natural size relative to fabric weave. Shallow depth of field, "
                    "organic lighting, high-end brand quality."
                ),
            },
            {
                "key": "09_model_scarf_lifestyle",
                "label": "Model — Scarf Accessory",
                "shot": (
                    "The brooch pinned to a scarf worn by a real woman. "
                    "Natural window light, realistic fabric textures, authentic luxury feel."
                ),
            },
        ],
    },
}

ALIASES = {
    "rings": "ring", "necklaces": "necklace", "chain": "necklace",
    "bracelets": "bracelet", "earrings": "earring", "studs": "earring",
    "hoops": "earring", "pendants": "pendant", "charm": "pendant",
    "bangles": "bangle", "cuff": "bangle", "anklets": "anklet",
    "brooches": "brooch", "pin": "brooch",
}

def resolve_category(raw: str) -> str:
    key = ALIASES.get(raw.strip().lower(), raw.strip().lower())
    if key not in CATEGORIES:
        raise ValueError(f"Unknown category: '{raw}'")
    return key


async def extract_design_lock(
    client: genai.Client, img: bytes, mime: str, category: str, worn_on: str, shot_labels: list[str]
) -> tuple[str, str, list[str]]:
    print("Locking design details and picking best angles (optimized single-call)...")
    
    shots_list_text = "\n".join([f"- {label}" for label in shot_labels])
    
    # COMBINED SINGLE CALL: Description + Angle Analysis + Recommendations
    resp = await client.aio.models.generate_content(
        model=MODEL,
        contents=[
            types.Part.from_bytes(data=img, mime_type=mime),
            types.Part.from_text(text=f"""
Look at this {category} image very carefully. 
Your primary goal is POINT-TO-POINT fidelity. 
Perform the following technical analysis in one pass:

1. DESIGN DESCRIPTION:
Write a precise paragraph describing the metal, main stones, setting, and proportions.
Be extremely detailed about stone counts, stone positions (relative to each other), and exact cuts.
Mention the exact arrangement (e.g., "5 stones on the left, 5 on the right").
If it is a cluster or halo, count the stones precisely.
Start with: "This {category} has..."

2. ANGLE IDENTIFICATION:
Identify which of these standard camera angles best matches the reference image:
{shots_list_text}
- Unknown

3. SHOT RECOMMENDATIONS:
Select exactly {int(TOTAL_PRODUCT)} Product shots from the list above that would best showcase this design.
MANDATORY VARIETY RULES:
- DO NOT select the angle identified in Step 2.
- DO NOT select angles that are visually similar to the reference image.
- MUST provide a 360-degree coverage (e.g., if ref is Front, pick Top-Down, Side, and 3/4).
- Prioritize angles that reveal details NOT visible in the reference image.

Format your entire response exactly as follows:
DESCRIPTION: [Your paragraph here]
ANGLE: [The exact label of the original angle]
RECOMMENDED: [Label1], [Label2], [Label3]

STRICT RULE: DO NOT CHANGE THE DESIGN. DO NOT ADD OR REMOVE ANY DIAMOND OR DETAIL. SAME TO SAME.
"""),
        ],
        config=types.GenerateContentConfig(response_modalities=["TEXT"]),
    )
    
    full_text = "".join(
        p.text for p in resp.candidates[0].content.parts
        if hasattr(p, "text") and p.text
    ).strip()
    
    # Parse the combined response
    design_lock = "Unknown design"
    if "DESCRIPTION:" in full_text:
        design_lock = full_text.split("DESCRIPTION:")[1].split("ANGLE:")[0].strip()
        
    existing_angle = "Unknown"
    if "ANGLE:" in full_text:
        existing_angle = full_text.split("ANGLE:")[1].split("RECOMMENDED:")[0].strip()
        
    recommended_labels = []
    if "RECOMMENDED:" in full_text:
        rec_part = full_text.split("RECOMMENDED:")[1].strip()
        recs = rec_part.split(",")
        recommended_labels = [r.strip() for r in recs if r.strip()]
        
    return design_lock, existing_angle, recommended_labels


# Strict rules injected into every prompt
DESIGN_LOCK_RULES = f"""
ABSOLUTE RULES — POINT-TO-POINT FIDELITY:
1. REPRODUCE THE DESIGN EXACTLY: Every single point, curve, and stone MUST match the reference image.
2. NO CREATIVITY: Do NOT add, remove, or modify even a single microscopic detail.
3. DIAMOND FIDELITY: Every diamond's position, cut, and size must remain identical to the original.
4. METAL COLOR: Keep the metal color and finish (polished, matte, hammered) exactly as shown.
5. NO SPARKLES: Do not add artificial sparkles, lens flares, or AI-generated "glow".
6. SAME TO SAME: The goal is a perfect replica from a different angle, not an "improved" version.
7. DO NOT INVENT: If a detail isn't visible or described, do not invent one.

{GLOBAL_THEME_RULES}
"""

ANGLE_RULES = """
CRITICAL ANGLE OVERRIDE:
- You MUST completely ignore the camera angle from the provided reference image!
- The reference image is ONLY for learning the design (stones, metal, shape).
- Do NOT generate the same angle as the reference image under any circumstances!
- You MUST render the jewelry from the EXACT angle described in the "CAMERA ANGLE / SHOT COMPOSITION" section.
- If the instruction says "Top-Down", render it perfectly flat from above.
- If the instruction says "Macro Close-Up", zoom in directly.
- The angle is the absolute most important requirement of this task. Firing the exact same angle multiple times is a severe failure.
"""

REALISM_SCALE_RULE = """
CRITICAL REALISM AND SCALE RULES:
- The jewelry MUST appear at its true, real-world size relative to the body part
- Do NOT make the jewelry oversized, exaggerated, or blown up
- A ring is small — it fits snugly on a finger (17-19mm diameter)
- A pendant is small — it rests delicately on the chest (typically 15-30mm wide)
- A bracelet wraps a wrist naturally (not oversized)
- The jewelry should look exactly as it appears in real jewelry photographs
- Real human proportions: natural finger size, natural wrist size, natural neck size
- The final image must be indistinguishable from a real luxury jewelry brand photograph
"""

PHOTOGRAPHY_REALISM_RULES = """
STRICT PHOTOGRAPHY REALISM RULES:
1. RAW PHOTOGRAPHY STYLE: The image must look like a raw, unedited photograph from a high-end Leica or Hasselblad camera. No "AI glow" or plastic-looking surfaces.
2. NATURAL LIGHTING ONLY: Use side-window lighting, soft natural shadows, and organic light falloff. NO even studio lighting. NO artificial-looking point lights.
3. AUTHENTIC METAL TEXTURE: Metal (gold, silver, platinum) must show microscopic texture, subtle reflections, and natural polish — NOT perfectly smooth or liquid-looking.
4. TEXTURED BACKGROUNDS: Use realistic, high-end materials like textured linen, dark silk, organic wood, or honed marble. The background should have depth and grain.
5. REAL DEPTH OF FIELD: Macro shots MUST have a razor-thin depth of field with creamy bokeh (blurred background). Model shots should have natural eye-level focus.
6. FILM COLOR GRADING: Use natural, muted, organic color tones. NO oversaturation. No neon colors. The palette must feel expensive and understated.
"""


def apply_logo_overlay(image_path: Path):
    """
    Applies the Riolls logo to the bottom-right corner of the image.
    """
    if not os.path.exists(LOGO_PATH):
        print(f"Logo not found at {LOGO_PATH}, skipping watermark.")
        return

    try:
        with Image.open(image_path) as base_img:
            # Open logo and ensure it has an alpha channel
            logo = Image.open(LOGO_PATH).convert("RGBA")
            
            # Scale logo to ~12% width of the base image
            base_w, base_h = base_img.size
            logo_w, logo_h = logo.size
            scale_factor = (base_w * 0.12) / logo_w
            new_size = (int(logo_w * scale_factor), int(logo_h * scale_factor))
            logo = logo.resize(new_size, Image.Resampling.LANCZOS)
            
            # Position: Bottom-right with 5% padding
            padding_x = int(base_w * 0.05)
            padding_y = int(base_h * 0.05)
            pos_x = base_w - logo.width - padding_x
            pos_y = base_h - logo.height - padding_y
            
            # Create overlay
            overlay = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
            overlay.paste(logo, (pos_x, pos_y), logo)
            
            # Composite and save (preserve format)
            if base_img.mode != "RGBA":
                base_img = base_img.convert("RGBA")
            
            final_img = Image.alpha_composite(base_img, overlay)
            
            # Convert back if needed (e.g. for JPEG)
            if image_path.suffix.lower() in [".jpg", ".jpeg"]:
                final_img = final_img.convert("RGB")
                final_img.save(image_path, "JPEG", quality=95)
            else:
                final_img.save(image_path)
                
            print(f"Applied logo to {image_path.name}")
            
    except Exception as e:
        print(f"Error applying logo to {image_path}: {e}")

async def generate_image(
    client:      genai.Client,
    img:         bytes | None,
    mime:        str | None,
    design_lock: str,
    shot:        dict,
    out_dir:     Path,
    category:    str,
    worn_on:     str,
    is_model:    bool,
    session_id:  str
) -> dict | None:

    if is_model:
        prompt = f"""
{DESIGN_LOCK_RULES}

MANDATORY DESIGN FIDELITY FOR MODEL SHOT:
- ABSOLUTELY NO DESIGN DRIFT: Every stone, prong, and metal curve must be IDENTICAL to the reference.
- NO POSITION CHANGES: Do not move stones, do not change their relative positions.
- THE JEWELRY IS THE MASTER: The hand must adapt to the jewelry, NOT the other way around.
- "POINT-TO-POINT" ACCURACY: If the reference has 10 stones, the generation MUST have 10 stones in the exact same pattern.

JEWELRY PIECE TO RENDER ({category}, worn on {worn_on}):
{design_lock}

STRICT CONTEXT:
Study the description above and the reference image. Your goal is a perfect 1:1 replica of the jewelry design, just placed on a real human {worn_on}.

{REALISM_SCALE_RULE}

{PHOTOGRAPHY_REALISM_RULES}

{ANGLE_RULES}

CAMERA ANGLE / SHOT COMPOSITION:
{shot['shot']}
THIS CAMERA ANGLE IS MANDATORY. RENDER THIS PRECISE PERSPECTIVE.

ADDITIONAL REALISM RULES:
- Real human skin: natural texture, pores, warmth — NOT plastic or AI-smooth. Pores and fine lines must be visible.
- Natural lighting that looks like a real photograph taken by a professional photographer. Natural shadows are mandatory.
- The jewelry must match the reference image design exactly. No extra stones, no missing pieces.
- The overall image must be photorealistic and indistinguishable from a real photo.
"""
    else:
        prompt = f"""
You are generating a clean product jewelry photograph.

JEWELRY PIECE ({category}):
{design_lock}

The text below describes the exact piece. Study it carefully.

{DESIGN_LOCK_RULES}

{PHOTOGRAPHY_REALISM_RULES}

{ANGLE_RULES}

CAMERA ANGLE / SHOT COMPOSITION:
{shot['shot']}
THIS CAMERA ANGLE IS MANDATORY. RENDER THIS PRECISE PERSPECTIVE.

PRODUCT SHOT RULES:
- Soft directional natural lighting with organic shadows
- Use the background texture specified in the shot description
- The jewelry must match the reference image exactly. No extra stones, no missing pieces.
- Photorealistic quality, razor-sharp focus on the jewelry, shallow depth of field
"""

    try:
        req_contents = []
        if img and mime:
            req_contents.append(types.Part.from_bytes(data=img, mime_type=mime))
            
        req_contents.append(types.Part.from_text(text=prompt))
        
        resp = await client.aio.models.generate_content(
            model=MODEL,
            contents=req_contents,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
            ),
        )

        for part in resp.candidates[0].content.parts:
            # Safely check for inline_data to avoid type errors
            inline_data = getattr(part, "inline_data", None)
            if inline_data:
                out_bytes = inline_data.data
                mime_part = getattr(inline_data, "mime_type", "")
                ext       = "png" if "png" in mime_part else "jpg"
                filename  = f"{shot['key']}.{ext}"
                save_path = out_dir / filename
                save_path.write_bytes(out_bytes)
                
                # Apply Branding Watermark
                apply_logo_overlay(save_path)
                
                return {"url": f"/outputs/{session_id}/{filename}", "label": shot['label']}

        return None

    except Exception as e:
        print(f"Error generating {shot['label']}: {e}")
        return None


async def generate_shots(image_bytes: bytes, mime_type: str, category_raw: str, session_id: str) -> list[dict]:
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set.")

    category = resolve_category(category_raw)
    cat      = CATEGORIES[category]
    worn_on  = str(cat["worn_on"])
    
    # Correctly type all_cat_shots as a list of tuples (dict, bool)
    all_cat_shots: list[tuple[dict, bool]] = (
        [(s, False) for s in cat["product"]] +
        [(s, True)  for s in cat["model"]]
    )
    shot_labels = [s["label"] for s, _ in all_cat_shots]

    out_dir = Path("outputs") / session_id
    out_dir.mkdir(parents=True, exist_ok=True)

    client = genai.Client(api_key=GEMINI_API_KEY)

    design_lock, existing_angle, recommended_labels = await extract_design_lock(client, image_bytes, mime_type, category, worn_on, shot_labels)
    (out_dir / "design_lock.txt").write_text(design_lock + f"\n\nIdentified Existing Angle: {existing_angle}\nRecommended: {recommended_labels}", encoding="utf-8")

    # Filter out the existing angle to ensure we don't duplicate it
    # We use a stricter check: if the label contains any part of the identified angle
    def is_angle_excluded(label: str, existing: str) -> bool:
        if existing.lower() == "unknown": return False
        l_low = label.lower()
        e_low = existing.lower()
        # If the identified angle is "Product — Front", exclude anything with "front"
        keywords = ["front", "side", "top", "back", "macro", "profile", "hand"]
        for kw in keywords:
            if kw in e_low and kw in l_low:
                return True
        return e_low in l_low or l_low in e_low

    available_shots = [(s, is_m) for s, is_m in all_cat_shots if not is_angle_excluded(s["label"], existing_angle)]
    
    # If filtering was too aggressive, fall back to simple exclusion
    if not available_shots:
        available_shots = [(s, is_m) for s, is_m in all_cat_shots if s["label"].lower() != existing_angle.lower()]
    
    # SHUFFLE available_shots to increase variety across different product runs
    random.shuffle(available_shots)
    
    product_shots = [x for x in available_shots if not x[1]]
    model_shots = [x for x in available_shots if x[1]]
    
    selected_shots: list = []
    
    # Process AI recommendations
    ai_selected_products: list = []
    ai_selected_models: list = []
    
    for rec_label in recommended_labels:
        for shot_tuple in available_shots:
            s, is_m = shot_tuple
            if s["label"].lower() in rec_label.lower() or rec_label.lower() in s["label"].lower():
                if is_m and shot_tuple not in ai_selected_models:
                    ai_selected_models.append(shot_tuple)
                elif not is_m and shot_tuple not in ai_selected_products:
                    ai_selected_products.append(shot_tuple)
                    
    # Pick Product Shots (Goal: TOTAL_PRODUCT)
    selected_shots.extend(ai_selected_products[:int(TOTAL_PRODUCT)])
    if len(selected_shots) < int(TOTAL_PRODUCT):
        remaining_prod = [x for x in product_shots if x not in selected_shots]
        selected_shots.extend(remaining_prod[:int(TOTAL_PRODUCT) - len(selected_shots)])
        
    # Pick Model Shots (Goal: TOTAL_MODEL)
    current_model_count = len([x for x in selected_shots if x[1]])
    
    selected_models_from_ai = ai_selected_models[:int(TOTAL_MODEL)]
    for m_shot in selected_models_from_ai:
        if m_shot not in selected_shots:
            selected_shots.append(m_shot)
            
    current_model_count = len([x for x in selected_shots if x[1]])
    if current_model_count < int(TOTAL_MODEL):
        remaining_model = [x for x in model_shots if x not in selected_shots]
        selected_shots.extend(remaining_model[:int(TOTAL_MODEL) - current_model_count])

    # Final target check
    total_target = int(TOTAL_PRODUCT) + int(TOTAL_MODEL)
    if len(selected_shots) < total_target:
        remaining = [x for x in available_shots if x not in selected_shots]
        selected_shots.extend(remaining[:int(total_target) - len(selected_shots)])

    # Process 2 shots at a time to prevent server overload
    final_results = []
    chunk_size = 2
    for i in range(0, len(selected_shots), chunk_size):
        chunk = selected_shots[i : i + chunk_size]
        chunk_results = await asyncio.gather(*[
            generate_image(client, image_bytes, mime_type, design_lock, s, out_dir, category, worn_on, is_m, session_id)
            for s, is_m in chunk
        ], return_exceptions=True)
        final_results.extend(chunk_results)

    # Filter out exceptions and Nones
    return [r for r in final_results if isinstance(r, dict)]

async def generate_shots_from_text(prompt_text: str, category_raw: str, session_id: str) -> list[dict]:
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set.")

    category = resolve_category(category_raw)
    cat      = CATEGORIES[category]
    worn_on  = str(cat["worn_on"])
    
    product_shots: list = [(s, False) for s in cat["product"]]
    model_shots: list = [(s, True) for s in cat["model"]]
    
    # Shuffle for variety
    random.shuffle(product_shots)
    random.shuffle(model_shots)
    
    selected_shots: list = []
    selected_shots.extend(product_shots[:int(TOTAL_PRODUCT)])
    selected_shots.extend(model_shots[:int(TOTAL_MODEL)])
    
    total_target = int(TOTAL_PRODUCT) + int(TOTAL_MODEL)
    if len(selected_shots) < int(total_target):
        remaining = [x for x in (product_shots + model_shots) if x not in selected_shots]
        selected_shots.extend(remaining[:int(total_target) - len(selected_shots)])

    out_dir = Path("outputs") / session_id
    out_dir.mkdir(parents=True, exist_ok=True)

    client = genai.Client(api_key=GEMINI_API_KEY)
    design_lock = prompt_text
    (out_dir / "design_lock.txt").write_text(design_lock, encoding="utf-8")

    final_results = []
    chunk_size = 2
    for i in range(0, len(selected_shots), chunk_size):
        chunk = selected_shots[i : i + chunk_size]
        chunk_results = await asyncio.gather(*[
            generate_image(client, None, None, design_lock, s, out_dir, category, worn_on, is_m, session_id)
            for s, is_m in chunk
        ], return_exceptions=True)
        final_results.extend(chunk_results)

    return [r for r in final_results if isinstance(r, dict)]
