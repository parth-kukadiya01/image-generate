import os
import asyncio
import mimetypes
from pathlib import Path
from google import genai
from google.genai import types

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDguSjewpyBF19U0JSuq4ZOPfDk3RZKeHU")
MODEL          = "gemini-2.5-flash-image"
TOTAL_PRODUCT  = 4
TOTAL_MODEL    = 2


CATEGORIES = {
    # ── RING ──────────────────────────────────────────────────────────────────
    "ring": {
        "worn_on": "ring finger",
        "product": [
            {
                "key":   "01_product_front",
                "label": "Product — Straight Front",
                "shot":  (
                    "The ring standing upright on a soft light grey neutral surface, shot straight-on "
                    "from the front at eye level. The face of the ring fills the frame symmetrically. "
                    "Soft even studio lighting. Soft light grey neutral background. Classic hero product shot."
                ),
            },
            {
                "key":   "02_product_glamour",
                "label": "Product — Glamour 45°",
                "shot":  (
                    "The ring standing upright, shot from a 45-degree front-left angle, "
                    "camera slightly above looking down. Shows the face, depth of setting, "
                    "and curve of band simultaneously. Dramatic studio lighting, Soft light grey neutral background."
                ),
            },
            {
                "key":   "03_product_top_down",
                "label": "Product — Top-Down",
                "shot":  (
                    "The ring lying flat, shot from directly above (top-down bird's-eye view). "
                    "Full face of the center stone, halo, and band fully visible. "
                    "Perfect symmetry visible. Soft light grey neutral background, even overhead lighting."
                ),
            },
            {
                "key":   "04_product_side",
                "label": "Product — Side Profile",
                "shot":  (
                    "The ring standing upright, shot from a strict 90-degree side profile. "
                    "Shows the full height of the setting above the band and the band depth. "
                    "Soft light grey neutral background, soft studio lighting."
                ),
            },
            {
                "key":   "07_product_macro",
                "label": "Product — Setting Macro Close-Up",
                "shot":  (
                    "Extreme macro close-up of the main stone setting on a neutral soft grey surface. "
                    "Focus entirely on the prongs, gallery, and exact center stone cuts. "
                    "Soft light grey background, sharp focus."
                ),
            },
            {
                "key":   "08_product_laying_glamour",
                "label": "Product — Laying Angle",
                "shot":  (
                    "The ring laying on its side at a dynamic 45-degree angle. "
                    "Shows the entire band resting against the surface and the face tilted elegantly toward the lens. "
                    "Soft light grey background, even studio lighting."
                ),
            },
        ],
        "model": [
            {
                "key":   "05_model_hand_front",
                "label": "Model — Hand Front",
                "shot":  (
                    "A real female hand with natural skin tone and neat nude-polished nails. "
                    "The ring sits on the ring finger at its REAL, natural size — a ring is small, "
                    "approximately 17-19mm diameter, fitting snugly on the finger. "
                    "Hand raised gracefully, fingers together, shot straight-on. "
                    "Clean neutral background, soft natural studio light. "
                    "The ring is clearly visible but proportionate — not oversized, not cartoonish. "
                    "Looks like a genuine luxury jewelry editorial photograph."
                ),
            },
            {
                "key":   "06_model_hand_glamour",
                "label": "Model — Hand Glamour",
                "shot":  (
                    "A real female hand with natural skin and nude nails, "
                    "held at a graceful 45-degree angle with fingers softly curved. "
                    "The ring is on the ring finger at its correct natural size — "
                    "small and elegant as a real ring appears on a real finger. "
                    "Shot from slightly above and to the side. Soft bokeh background. "
                    "The ring catches the light naturally. Photorealistic luxury jewelry advertisement — "
                    "real proportions, real scale, human and elegant."
                ),
            },
            {
                "key":   "09_model_hand_holding",
                "label": "Model — Cupped Hand Action",
                "shot":  (
                    "A real female hand gently cupping or adjusting something with the other hand, focusing on the ring finger. "
                    "The ring sparkles naturally in motion. "
                    "Real natural skin tones. Soft natural studio light, out-of-focus bokeh background. Photorealistic lifestyle setting."
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
                    "The necklace hanging vertically as if around a neck, shot straight-on. "
                    "Chain drapes naturally, pendant centered at the bottom. "
                    "Soft light grey neutral background, even studio lighting. Classic product shot."
                ),
            },
            {
                "key":   "02_product_flat_lay",
                "label": "Product — Flat Lay",
                "shot":  (
                    "The necklace laid flat on a soft light grey neutral surface, shot top-down from directly above. "
                    "Chain arranged in a clean arc with pendant centered. "
                    "Even overhead lighting. Shows full length and pendant detail."
                ),
            },
            {
                "key":   "03_product_pendant_close",
                "label": "Product — Pendant Close-Up",
                "shot":  (
                    "Close-up of the pendant only, shot straight-on from the front. "
                    "Fills most of the frame. All stone facets and metal details razor-sharp. "
                    "Soft light grey neutral background, dramatic studio lighting."
                ),
            },
            {
                "key":   "04_product_glamour",
                "label": "Product — Glamour 45°",
                "shot":  (
                    "The necklace hanging, shot from a 45-degree glamour angle slightly elevated. "
                    "Shows pendant depth and chain drape beautifully. "
                    "Soft light grey neutral background, dramatic studio lighting."
                ),
            },
            {
                "key":   "07_product_chain_detail",
                "label": "Product — Clasp & Chain Lay",
                "shot":  (
                    "The necklace laid down, creatively spiraled to feature the clasp ending next to the pendant. "
                    "Highlights the delicate chain link texture and closure setup. "
                    "Soft light grey neutral background, sharp studio focus."
                ),
            },
            {
                "key":   "08_product_dynamic_drape",
                "label": "Product — Asymmetric Drape",
                "shot":  (
                    "The necklace elegantly draped over an angular, soft white stone or neutral prop. "
                    "Pendant rests cleanly on the surface while the chain flows diagonally. "
                    "Soft directional light, distinct shadow, highly curated presentation."
                ),
            },
        ],
        "model": [
            {
                "key":   "05_model_neck_front",
                "label": "Model — Neck Front",
                "shot":  (
                    "A real woman wearing the necklace, shot from the front framing collarbone to chin. "
                    "The necklace rests at its NATURAL size on her bare collarbone — "
                    "a necklace pendant is typically 15-30mm, fitting naturally on the neck. "
                    "It should NOT appear oversized or exaggerated. "
                    "Soft natural studio lighting, clean neutral background. "
                    "Necklace in sharp focus. Looks like a real jewelry brand photograph."
                ),
            },
            {
                "key":   "06_model_pendant_macro",
                "label": "Model — Pendant Close-Up",
                "shot":  (
                    "Close-up of the pendant resting on a real woman's collarbone. "
                    "The pendant is at its REAL, natural scale — not blown up or exaggerated. "
                    "Shallow depth of field — pendant in razor-sharp focus, skin softly blurred. "
                    "Warm natural light, real skin texture visible. Authentic luxury editorial style."
                ),
            },
            {
                "key":   "09_model_clothing_lifestyle",
                "label": "Model — Over Clothing Lifestyle",
                "shot":  (
                    "A real woman wearing a silky neutral-toned blouse or fine knit sweater, with the necklace resting elegantly over the fabric. "
                    "The chain and pendant are at realistic scales. "
                    "Natural window lighting, shallow depth of field. High-end lifestyle vibe."
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
                    "The bracelet standing upright on a soft light grey neutral surface, shot straight-on. "
                    "Full width and all stones visible. Soft light grey neutral background, even studio lighting."
                ),
            },
            {
                "key":   "02_product_glamour",
                "label": "Product — Glamour 45°",
                "shot":  (
                    "The bracelet at a 45-degree angle, camera slightly elevated. "
                    "Shows the front face and side depth simultaneously. "
                    "Soft light grey neutral background, dramatic studio lighting."
                ),
            },
            {
                "key":   "03_product_top_down",
                "label": "Product — Top-Down",
                "shot":  (
                    "The bracelet lying flat, shot from directly above (top-down). "
                    "Full stone arrangement and width visible. Soft light grey neutral background."
                ),
            },
            {
                "key":   "04_product_detail",
                "label": "Product — Clasp Detail",
                "shot":  (
                    "Close-up of the bracelet clasp and end section. "
                    "Shows the craftsmanship and closure mechanism. "
                    "Soft light grey neutral background, sharp studio lighting."
                ),
            },
        ],
        "model": [
            {
                "key":   "05_model_wrist_front",
                "label": "Model — Wrist Front",
                "shot":  (
                    "A real female wrist and hand, natural skin, neat nails. "
                    "The bracelet sits naturally on the wrist at its REAL size — "
                    "a bracelet wraps a 15-17cm wrist comfortably, not oversized. "
                    "Hand held gracefully, shot front-on. "
                    "Clean neutral background, soft studio light. Bracelet in sharp focus. "
                    "Photorealistic — real wrist, real proportions."
                ),
            },
            {
                "key":   "06_model_wrist_lifestyle",
                "label": "Model — Wrist Lifestyle",
                "shot":  (
                    "A real woman's wrist with the bracelet at its natural, realistic size. "
                    "Hand resting naturally on a clean surface. "
                    "Shot at a relaxed 45-degree angle. Soft natural light, softly blurred background. "
                    "Looks like a real lifestyle jewelry photograph — natural proportions, not exaggerated."
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
                    "Both earrings as a matching pair, laid on a soft light grey neutral surface side by side. "
                    "Shot straight-on from the front. "
                    "Soft light grey neutral background, even studio lighting. Full detail visible."
                ),
            },
            {
                "key":   "02_product_single_glamour",
                "label": "Product — Single Glamour",
                "shot":  (
                    "One single earring, shot from a 45-degree glamour angle, camera slightly elevated. "
                    "Soft light grey neutral background, dramatic studio lighting. Every stone facet visible."
                ),
            },
            {
                "key":   "03_product_top_down",
                "label": "Product — Pair Top-Down",
                "shot":  (
                    "Both earrings laid flat, shot from directly above (top-down). "
                    "Symmetrically placed. Full surface detail visible. Soft light grey neutral background."
                ),
            },
            {
                "key":   "04_product_side",
                "label": "Product — Single Side Profile",
                "shot":  (
                    "One single earring, shot from a 90-degree side profile. "
                    "Shows the depth, backing, and drop length. Soft light grey neutral background."
                ),
            },
            {
                "key":   "07_product_creative_tilt",
                "label": "Product — Pair Tilt Profile",
                "shot":  (
                    "Both earrings standing dynamically, offset from each other. "
                    "One turned slightly sideways to show depth, the other facing forward. "
                    "Soft studio gradient grey background, precise edge lighting."
                ),
            },
            {
                "key":   "08_product_macro_back",
                "label": "Product — Backing Texture Detail",
                "shot":  (
                    "Extreme macro shot of the post/hook and back design of a single earring. "
                    "Every metallic slope and clasp detail sharply rendered. "
                    "Clear soft grey background, dramatic lighting."
                ),
            },
        ],
        "model": [
            {
                "key":   "05_model_ear_side",
                "label": "Model — Ear Side Profile",
                "shot":  (
                    "A real woman's ear and side of her face, hair swept back to show the earring. "
                    "The earring is at its REAL natural size — earrings hang from the earlobe and "
                    "should look proportionate to the face and ear, not oversized. "
                    "Shot from a clean side-profile angle. Soft natural studio light, clean background. "
                    "Earring in sharp focus. Photorealistic."
                ),
            },
            {
                "key":   "06_model_ear_34",
                "label": "Model — Face 3/4 Angle",
                "shot":  (
                    "A real woman at a three-quarter face angle, earring visible on her ear. "
                    "The earring is realistically sized — proportionate to her ear and face, "
                    "as a real earring looks in a real photo. Natural expression, relaxed. "
                    "Soft studio light with bokeh background. Earring in sharp focus."
                ),
            },
            {
                "key":   "09_model_windswept_action",
                "label": "Model — Lifestyle Action Hair",
                "shot":  (
                    "A woman's profile with her hand brushing a single strand of hair behind her ear, clearly revealing the earring. "
                    "Earring catches the light perfectly. Realistic natural skin and proportion. "
                    "Warm natural daylight, lifestyle atmosphere, cinematic crop."
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
                    "The pendant alone (no chain), shot straight-on from the front at eye level. "
                    "All stone and metal details fully visible. Soft light grey neutral background, even studio lighting."
                ),
            },
            {
                "key":   "02_product_glamour",
                "label": "Product — Pendant Glamour 45°",
                "shot":  (
                    "The pendant hanging on its chain, shot from a 45-degree glamour angle, slightly elevated. "
                    "Shows depth, bail, and how pendant hangs.Soft light grey neutral background."
                ),
            },
            {
                "key":   "03_product_top_down",
                "label": "Product — Top-Down",
                "shot":  (
                    "The pendant lying flat, shot from directly above. "
                    "Full surface layout visible. Soft light grey neutral background."
                ),
            },
            {
                "key":   "04_product_back",
                "label": "Product — Back Detail",
                "shot":  (
                    "The back of the pendant shown clearly. "
                    "Shows any engravings, bail attachment, or back plate. "
                    "Soft light grey neutral background, even studio lighting."
                ),
            },
        ],
        "model": [
            {
                "key":   "05_model_collarbone",
                "label": "Model — Pendant on Collarbone",
                "shot":  (
                    "A real woman wearing the pendant on her neck. "
                    "Shot from the front, framing collarbone to chin. "
                    "The pendant rests naturally on her collarbone at its REAL, natural size — "
                    "a pendant is typically 15-30mm wide, sitting small and elegant on the chest. "
                    "It must NOT appear oversized or exaggerated — it should look exactly as "
                    "a real pendant looks around a real person's neck in a real photograph. "
                    "Soft studio light, clean neutral background. Pendant in sharp focus."
                ),
            },
            {
                "key":   "06_model_pendant_macro",
                "label": "Model — Pendant Macro Close-Up",
                "shot":  (
                    "Close-up photograph of the pendant resting on a real woman's chest/collarbone. "
                    "The pendant is at its TRUE, REAL-WORLD SIZE relative to the skin — "
                    "small and delicate as it actually appears in real life. "
                    "Shallow depth of field — pendant razor-sharp, skin softly blurred. "
                    "Warm natural light. Real skin texture. Feels like a genuine editorial jewelry photo."
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
                    "The bangle standing upright on a soft light grey neutral surface, shot straight-on. "
                    "Full circle and all stones visible. Soft light grey neutral background, even studio lighting."
                ),
            },
            {
                "key":   "02_product_top_down",
                "label": "Product — Top-Down",
                "shot":  (
                    "The bangle lying flat, shot from directly above (top-down). "
                    "Full circle and all surface details visible. Soft light grey neutral background."
                ),
            },
            {
                "key":   "03_product_glamour",
                "label": "Product — Glamour 45°",
                "shot":  (
                    "The bangle at a 45-degree glamour angle, camera slightly elevated. "
                    "Shows stones and depth simultaneously. Soft light grey neutral background."
                ),
            },
            {
                "key":   "04_product_side",
                "label": "Product — Side Profile",
                "shot":  (
                    "The bangle standing upright, shot from a 90-degree side profile. "
                    "Shows the width, stone arrangement along the edge. Soft light grey neutral background."
                ),
            },
        ],
        "model": [
            {
                "key":   "05_model_wrist_front",
                "label": "Model — Wrist Front",
                "shot":  (
                    "A real female wrist, natural skin, bangle at its REAL natural size. "
                    "A bangle is a rigid circle that fits around the wrist, typically 60-65mm diameter — "
                    "it should look proportionate on the wrist, not oversized. "
                    "Hand gracefully posed, shot front-on. Clean neutral background, soft studio light."
                ),
            },
            {
                "key":   "06_model_wrist_lifestyle",
                "label": "Model — Wrist Lifestyle",
                "shot":  (
                    "A real woman's wrist with the bangle at realistic scale, hand resting naturally. "
                    "Soft natural light, blurred background. Candid, real lifestyle feel. "
                    "The bangle is sized correctly as it would appear in a real photograph."
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
                    "The anklet laid flat on a soft light grey neutral surface, chain in a natural arc. "
                    "Shot top-down from directly above. Full length and all details visible."
                ),
            },
            {
                "key":   "02_product_glamour",
                "label": "Product — Glamour Angle",
                "shot":  (
                    "The anklet draped naturally, shot from a 45-degree angle. "
                    "Shows depth and any charms or stones. Soft light grey neutral background."
                ),
            },
            {
                "key":   "03_product_hanging",
                "label": "Product — Hanging Display",
                "shot":  (
                    "The anklet hanging vertically as if on an ankle, shot straight-on. "
                    "Full length of chain visible. Soft light grey neutral background."
                ),
            },
            {
                "key":   "04_product_charm_close",
                "label": "Product — Charm/Stone Close-Up",
                "shot":  (
                    "Close-up of any charms or stones on the anklet. "
                    "Every detail sharp. Soft light grey neutral background, macro studio lighting."
                ),
            },
        ],
        "model": [
            {
                "key":   "05_model_ankle_front",
                "label": "Model — Ankle Front",
                "shot":  (
                    "A real woman's ankle and foot, natural skin. "
                    "The anklet sits naturally around the ankle at its REAL size — "
                    "an anklet wraps a 20-25cm ankle, delicate and proportionate. "
                    "Foot gracefully pointed or relaxed. Shot front-on. "
                    "Clean background, soft natural light. Anklet in sharp focus. Real, human."
                ),
            },
            {
                "key":   "06_model_ankle_lifestyle",
                "label": "Model — Ankle Lifestyle",
                "shot":  (
                    "A real woman relaxing, anklet at its natural, realistic scale on her ankle. "
                    "She may be seated with legs extended, or on soft fabric. "
                    "Natural soft light, soft background. Candid, real lifestyle feel."
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
                    "The brooch flat on a soft light grey neutral surface, shot top-down from directly above. "
                    "All stones and metalwork fully visible, perfect symmetry. "
                    "Even studio lighting. Soft light grey neutral background."
                ),
            },
            {
                "key":   "02_product_glamour",
                "label": "Product — Glamour Angle",
                "shot":  (
                    "The brooch propped at a slight angle, shot from 45 degrees, camera slightly elevated. "
                    "Shows face, depth, and dimension. Dramatic studio lighting,"
                ),
            },
            {
                "key":   "03_product_side",
                "label": "Product — Side Profile",
                "shot":  (
                    "The brooch shot from a 90-degree side profile. "
                    "Shows the pin mechanism and depth of the piece. Soft light grey neutral background."
                ),
            },
            {
                "key":   "04_product_stone_close",
                "label": "Product — Stone Close-Up",
                "shot":  (
                    "Extreme close-up of the brooch stones and setting. Every facet visible. "
                    "Soft light grey neutral background, macro studio lighting."
                ),
            },
        ],
        "model": [
            {
                "key":   "05_model_lapel_front",
                "label": "Model — Lapel Front",
                "shot":  (
                    "A real woman wearing the brooch pinned on the lapel of a blazer or coat. "
                    "The brooch is at its REAL natural size — proportionate to the lapel, "
                    "not oversized or exaggerated. Shot straight-on from the front. "
                    "Soft studio light, neutral background. Natural, elegant, photorealistic."
                ),
            },
            {
                "key":   "06_model_lapel_close",
                "label": "Model — Lapel Close-Up",
                "shot":  (
                    "Close-up of the brooch pinned on a real woman's lapel or jacket. "
                    "The brooch appears at its true, real-world scale on the fabric. "
                    "Brooch in sharp focus, fabric texture visible. Shallow depth of field. "
                    "Natural light. Genuine editorial jewelry photography style."
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
    print("Locking design details and picking best angles (simplified)...")
    
    # First: Get a pure, precise description of the design (like generate_images.py)
    desc_resp = await client.aio.models.generate_content(
        model=MODEL,
        contents=[
            types.Part.from_bytes(data=img, mime_type=mime),
            types.Part.from_text(text=f"""
Look at this {category} image very carefully.
Describe ONLY what you actually see — do not invent, add, or assume anything.

Write a precise description covering:
1. Metal: exact color and finish as it appears in the image
2. Main stone(s): exact shape, cut, color, size as visible
3. Setting: exactly as it appears (prong count, halo, bezel, etc.)
4. Secondary stones: exactly as visible (placement, size, cut)
5. Band/chain/structure: exactly as it appears
6. Any visible engravings, texture, or decorative elements
7. Overall shape, size, and proportions as seen in the image

Start with: "This {category} has..."
Describe only what is visible. Do not add anything not in the image.
Write as one paragraph. Be precise and specific about actual dimensions and scale.
"""),
        ],
        config=types.GenerateContentConfig(response_modalities=["TEXT"]),
    )
    design_lock = "".join(
        p.text for p in desc_resp.candidates[0].content.parts
        if hasattr(p, "text") and p.text
    ).strip()
    
    # Second: Briefly ask for the existing angle and recommendations, feeding it the description
    shots_list_text = "\n".join([f"- {label}" for label in shot_labels])
    angle_resp = await client.aio.models.generate_content(
        model=MODEL,
        contents=[
            types.Part.from_bytes(data=img, mime_type=mime),
            types.Part.from_text(text=f"""
Based on this {category} image:
1. Identify which of the following standard camera angles best matches the reference image:
{shots_list_text}
- Unknown

2. Based on the unique geometry and design, please carefully select exactly {TOTAL_PRODUCT} strictly Product shots and exactly {TOTAL_MODEL} strictly Model shots from the list above that will present this exact item perfectly in an e-commerce gallery. Do not recommend the "Unknown" angle or the exact angle you identified as the original image's angle. Format your picks exactly as:
RECOMMENDED: [Label1], [Label2], [Label3], etc.

At the very end of your response, you MUST append:
ANGLE: [The exact label of the original angle]
"""),
        ],
        config=types.GenerateContentConfig(response_modalities=["TEXT"]),
    )
    
    angle_text = "".join(
        p.text for p in angle_resp.candidates[0].content.parts
        if hasattr(p, "text") and p.text
    ).strip()
    
    parts = angle_text.split("ANGLE:")
    existing_angle = parts[1].strip() if len(parts) > 1 else "Unknown"
    
    recommended_labels = []
    if "RECOMMENDED:" in angle_text:
        rec_part = angle_text.split("RECOMMENDED:")[1].split("ANGLE:")[0]
        recs = rec_part.strip().split(",")
        recommended_labels = [r.strip() for r in recs if r.strip()]
        
    return design_lock, existing_angle, recommended_labels


# Strict rules injected into every prompt
DESIGN_LOCK_RULES = """
ABSOLUTE RULES — MUST NOT BE BROKEN:
1. Reproduce ONLY what is described above and shown in the reference image
2. Do NOT add any stone, element, or detail not in the reference
3. Do NOT remove any stone, element, or detail that IS in the reference
4. Do NOT change the metal color — keep it exactly as in the reference
5. Do NOT change any stone color, shape, or cut
6. Do NOT change proportions, dimensions, or silhouette
7. Do NOT "improve", "simplify", or "stylize" the design in any way
8. Reproduce it exactly — a faithful render, not a reinterpretation
9. NO SPARKLES ALLOWED: Do not draw artificial starbursts, lens flares, or exaggerated AI sparkles on the diamonds. The stones must look like real, raw photography.
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
You are generating a REALISTIC jewelry photograph for a luxury brand.

JEWELRY PIECE ({category}, worn on {worn_on}):
{design_lock}

The text below describes the exact piece. Study it carefully.

{DESIGN_LOCK_RULES}

{REALISM_SCALE_RULE}

{ANGLE_RULES}

CAMERA ANGLE / SHOT COMPOSITION:
{shot['shot']}
THIS CAMERA ANGLE IS MANDATORY. RENDER THIS PRECISE PERSPECTIVE.

ADDITIONAL REALISM RULES:
- Real human skin: natural texture, pores, warmth — NOT plastic or AI-smooth
- Natural lighting that looks like a real photograph taken by a professional photographer
- The jewelry must match the reference image design exactly
- The overall image must be photorealistic and indistinguishable from a real photo
"""
    else:
        prompt = f"""
You are generating a clean product jewelry photograph.

JEWELRY PIECE ({category}):
{design_lock}

The text below describes the exact piece. Study it carefully.

{DESIGN_LOCK_RULES}

{ANGLE_RULES}

CAMERA ANGLE / SHOT COMPOSITION:
{shot['shot']}
THIS CAMERA ANGLE IS MANDATORY. RENDER THIS PRECISE PERSPECTIVE.

PRODUCT SHOT RULES:
- Soft light grey or warm cream neutral background (NOT pure white)
- Professional studio lighting with soft gradient shadow beneath the piece
- The jewelry must match the reference image exactly
- Photorealistic quality, sharp focus on the jewelry
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
            if getattr(part, "inline_data", None):
                out_bytes = part.inline_data.data
                ext       = "png" if "png" in getattr(part.inline_data, "mime_type", "") else "jpg"
                filename  = f"{shot['key']}.{ext}"
                save_path = out_dir / filename
                save_path.write_bytes(out_bytes)
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
    worn_on  = cat["worn_on"]
    
    all_cat_shots = (
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
    available_shots = [(s, is_m) for s, is_m in all_cat_shots if s["label"].lower() not in existing_angle.lower()]
    
    product_shots = [x for x in available_shots if not x[1]]
    model_shots = [x for x in available_shots if x[1]]
    
    selected_shots = []
    
    # Process AI recommendations
    ai_selected_products = []
    ai_selected_models = []
    
    for rec_label in recommended_labels:
        for shot_tuple in available_shots:
            s, is_m = shot_tuple
            if s["label"].lower() in rec_label.lower() or rec_label.lower() in s["label"].lower():
                if is_m and shot_tuple not in ai_selected_models:
                    ai_selected_models.append(shot_tuple)
                elif not is_m and shot_tuple not in ai_selected_products:
                    ai_selected_products.append(shot_tuple)
                    
    # Pick Product Shots (Goal: TOTAL_PRODUCT)
    selected_shots.extend(ai_selected_products[:TOTAL_PRODUCT])
    if len(selected_shots) < TOTAL_PRODUCT:
        remaining_prod = [x for x in product_shots if x not in selected_shots]
        selected_shots.extend(remaining_prod[:TOTAL_PRODUCT - len(selected_shots)])
        
    # Pick Model Shots (Goal: TOTAL_MODEL)
    current_model_count = 0
    for shot in ai_selected_models[:TOTAL_MODEL]:
        selected_shots.append(shot)
        current_model_count += 1
        
    if current_model_count < TOTAL_MODEL:
        remaining_model = [x for x in model_shots if x not in selected_shots]
        selected_shots.extend(remaining_model[:TOTAL_MODEL - current_model_count])

    # If somehow we still haven't met the total target 6 (4+2), back-fill
    total_target = TOTAL_PRODUCT + TOTAL_MODEL
    if len(selected_shots) < total_target:
        remaining = [x for x in available_shots if x not in selected_shots]
        selected_shots.extend(remaining[:total_target - len(selected_shots)])

    results = await asyncio.gather(*[
        generate_image(client, image_bytes, mime_type, design_lock, shot, out_dir, category, worn_on, is_model, session_id)
        for shot, is_model in selected_shots
    ], return_exceptions=True)

    # Filter out exceptions and Nones
    valid_results = [r for r in results if isinstance(r, dict)]
    return valid_results

async def generate_shots_from_text(prompt_text: str, category_raw: str, session_id: str) -> list[dict]:
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set.")

    category = resolve_category(category_raw)
    cat      = CATEGORIES[category]
    worn_on  = cat["worn_on"]
    
    product_shots = [(s, False) for s in cat["product"]]
    model_shots = [(s, True) for s in cat["model"]]
    
    # Select EXACTLY 4 product and 2 model
    selected_shots = []
    
    if len(product_shots) >= TOTAL_PRODUCT:
        selected_shots.extend(product_shots[:TOTAL_PRODUCT])
    else:
        selected_shots.extend(product_shots)
        
    if len(model_shots) >= TOTAL_MODEL:
        selected_shots.extend(model_shots[:TOTAL_MODEL])
    else:
        selected_shots.extend(model_shots)
    
    total_target = TOTAL_PRODUCT + TOTAL_MODEL
    if len(selected_shots) < total_target:
        remaining = [x for x in (product_shots + model_shots) if x not in selected_shots]
        selected_shots.extend(remaining[:total_target - len(selected_shots)])

    out_dir = Path("outputs") / session_id
    out_dir.mkdir(parents=True, exist_ok=True)

    client = genai.Client(api_key=GEMINI_API_KEY)

    design_lock = prompt_text
    (out_dir / "design_lock.txt").write_text(design_lock, encoding="utf-8")

    results = await asyncio.gather(*[
        generate_image(client, None, None, design_lock, shot, out_dir, category, worn_on, is_model, session_id)
        for shot, is_model in selected_shots
    ], return_exceptions=True)

    # Filter out exceptions and Nones
    valid_results = [r for r in results if isinstance(r, dict)]
    return valid_results
