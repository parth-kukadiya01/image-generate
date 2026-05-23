import os
import asyncio
import mimetypes
import random
from pathlib import Path
from PIL import Image
from google import genai
from google.genai import types

# ── Central config (single source of truth) ───────────────────────────────────
from app.core.config import GEMINI_API_KEY, MODEL, TOTAL_PRODUCT, TOTAL_MODEL, LOGO_PATH

# ── Brand / prompt config ─────────────────────────────────────────────────────
from app.core.prompt_config import CREATIVE_SCENES, GLOBAL_THEME_RULES, ALIASES, CATEGORIES




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
CRITICAL REALISM AND SCALE RULES — STRICT ENFORCEMENT:
- The jewelry MUST appear at its EXACT true real-world size. NO exceptions.
- NEVER make jewelry oversized, enlarged, or "hero" scaled. This is a HARD FAILURE.
- A ring: snug on a finger, 15–17mm outer diameter. The band is THIN.
- A pendant: delicate on chest, 10–25mm wide MAX. The chain is fine and thin.
- A bracelet: wraps the wrist snugly, NOT ballooned or oversized.
- An earring: small and delicate, proportional to the earlobe.
- A necklace chain: fine and thin, resting naturally against the collarbone.
- REFERENCE CHECK: Mentally compare the rendered jewelry to a real fingernail. 
  A ring should be no wider than 1–2 fingernails. A pendant no larger than a thumbnail.
- The image MUST be indistinguishable from a real luxury brand photograph.
- Oversized jewelry = complete generation failure. Render small and precise.
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

MODEL_IDENTITY_LOCK = """
MODEL IDENTITY LOCK (CRITICAL):
You MUST use the exact same male model for every single model shot. Identity is locked:
- Gender: Male
- Ethnicity: Caucasian / Western European
- Build: Lean, well-proportioned, natural hands with defined knuckles
- Skin Tone: Fair to light-medium, natural, un-airbrushed
- Hands: Clean, trimmed nails, natural masculine hand proportions
- Vibe: Quiet luxury, minimal, high-end menswear editorial
DO NOT USE A FEMALE MODEL. DO NOT CHANGE ETHNICITY. MUST BE THIS EXACT MALE EVERY TIME.
"""

EARRING_SCALE_RULE = """
EARRING SCALE ENFORCEMENT — CRITICAL:
- A stud earring is 1–2mm in diameter. Roughly the size of a pencil eraser.
- A drop/dangle earring is 5–10mm long MAX. No longer than a thumbnail.
- A hoop earring is 5–10mm inner diameter. Delicate and thin wire.
- The earring must look TINY and delicate — not like a brooch or pendant.
- ALWAYS show the earlobe in model shots so the viewer has a size reference.
- In product shots: place the earring next to a prop (marble surface, small flower petal,
  or linen fabric texture) so the scale is grounded. The earring should look small against it.
- HARD RULE: If the earring fills more than 5% of the image frame in a product shot, it is WRONG.
- HARD RULE: In model shots, the earring must not extend below the jawline unless it is
  explicitly a long chandelier earring (60mm+).
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
        category_scale_note = ""
        if "earring" in category.lower():
            print("::::::::::")
            category_scale_note = EARRING_SCALE_RULE
        SCALE_ANCHOR = f"""
SCALE ANCHOR — READ BEFORE GENERATING:
- This is a {category} worn on {worn_on}.
- Visualize a REAL human {worn_on} at full natural size.
- The jewelry occupies only a SMALL fraction of that body part.
- If the jewelry looks large or impressive in size, you have FAILED. Make it smaller.
- Final check: Would this jewelry look normal in a real Cartier or Tiffany catalog photo? 
  If yes, proceed. If the jewelry looks oversized, restart.
"""
        prompt = f"""
{DESIGN_LOCK_RULES}
{SCALE_ANCHOR}
{category_scale_note}
MANDATORY DESIGN FIDELITY FOR MODEL SHOT:
- ABSOLUTELY NO DESIGN DRIFT: You must use the attached reference image as the absolute source of truth for the jewelry design.
- DO NOT invent or alter any engravings, patterns, thickness, or stones.
- THE JEWELRY IS THE MASTER: The hand must adapt to the jewelry, NOT the other way around.

JEWELRY PIECE TO RENDER:
Category: {category} (worn on {worn_on})
Design: EXACTLY AS SHOWN IN THE PROVIDED REFERENCE IMAGE. Do not rely on text descriptions for the design. Copy the image pixels.

{MODEL_IDENTITY_LOCK}

STRICT CONTEXT:
Your goal is a perfect 1:1 replica of the jewelry design shown in the reference image, worn by the specific model described above.

{REALISM_SCALE_RULE}

{PHOTOGRAPHY_REALISM_RULES}

{ANGLE_RULES}

CAMERA ANGLE / SHOT COMPOSITION:
{shot['shot']}
THIS CAMERA ANGLE IS MANDATORY. RENDER THIS PRECISE PERSPECTIVE.
"""
    else:
        prompt = f"""
You are generating a clean product jewelry photograph.

JEWELRY PIECE:
Category: {category}
Design: EXACTLY AS SHOWN IN THE PROVIDED REFERENCE IMAGE. Do not invent any details. Copy the reference image perfectly.

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


async def generate_shots(
    image_bytes: bytes,
    mime_type: str,
    category_raw: str,
    session_id: str,
    requested_shots: list[str] | None = None,
    mode: str = "standard",
) -> list[dict]:
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set.")

    category = resolve_category(category_raw)
    cat      = CATEGORIES[category]
    worn_on  = str(cat["worn_on"])

    # ── Build the pool of candidate shots depending on mode ───────────────────
    if mode == "social":
        # Social / creative mode: use the curated editorial scenes (all are product-style, not model)
        all_cat_shots: list[tuple[dict, bool]] = [(s, False) for s in CREATIVE_SCENES]
    else:
        # Standard mode: product angles + model shots for this category
        all_cat_shots = (
            [(s, False) for s in cat["product"]] +
            [(s, True)  for s in cat["model"]]
        )

    shot_labels = [s["label"] for s, _ in all_cat_shots]

    out_dir = Path("outputs") / session_id
    out_dir.mkdir(parents=True, exist_ok=True)

    client = genai.Client(api_key=GEMINI_API_KEY)

    design_lock, existing_angle, recommended_labels = await extract_design_lock(
        client, image_bytes, mime_type, category, worn_on, shot_labels
    )
    (out_dir / "design_lock.txt").write_text(
        design_lock + f"\n\nIdentified Existing Angle: {existing_angle}\nRecommended: {recommended_labels}",
        encoding="utf-8",
    )

    # ── If the user explicitly picked shots, honour them exactly ──────────────
    if requested_shots:
        key_set = set(requested_shots)
        final_shots: list = [(s, is_m) for s, is_m in all_cat_shots if s["key"] in key_set]
        # Fall back to all shots if none matched the keys
        if not final_shots:
            final_shots = list(all_cat_shots)
    else:
        # ── Filter out the angle already visible in the reference image ───────
        def is_angle_excluded(label: str, existing: str) -> bool:
            if existing.lower() == "unknown":
                return False
            l_low = label.lower()
            e_low = existing.lower()
            keywords = ["front", "side", "top", "back", "macro", "profile", "hand"]
            for kw in keywords:
                if kw in e_low and kw in l_low:
                    return True
            return e_low in l_low or l_low in e_low

        available = [(s, is_m) for s, is_m in all_cat_shots if not is_angle_excluded(s["label"], existing_angle)]
        if not available:
            available = [(s, is_m) for s, is_m in all_cat_shots if s["label"].lower() != existing_angle.lower()]

        random.shuffle(available)

        product_pool = [x for x in available if not x[1]]
        model_pool   = [x for x in available if x[1]]

        final_shots = []

        # Match AI-recommended labels
        ai_products: list = []
        ai_models:   list = []
        for rec_label in recommended_labels:
            for shot_tuple in available:
                s, is_m = shot_tuple
                if s["label"].lower() in rec_label.lower() or rec_label.lower() in s["label"].lower():
                    if is_m and shot_tuple not in ai_models:
                        ai_models.append(shot_tuple)
                    elif not is_m and shot_tuple not in ai_products:
                        ai_products.append(shot_tuple)

        # Fill product slots
        final_shots.extend(ai_products[:int(TOTAL_PRODUCT)])
        if len(final_shots) < int(TOTAL_PRODUCT):
            remaining = [x for x in product_pool if x not in final_shots]
            final_shots.extend(remaining[:int(TOTAL_PRODUCT) - len(final_shots)])

        # Fill model slots
        for m in ai_models[:int(TOTAL_MODEL)]:
            if m not in final_shots:
                final_shots.append(m)
        cur_model = sum(1 for x in final_shots if x[1])
        if cur_model < int(TOTAL_MODEL):
            remaining = [x for x in model_pool if x not in final_shots]
            final_shots.extend(remaining[:int(TOTAL_MODEL) - cur_model])

        # Top-up if still short
        total_target = int(TOTAL_PRODUCT) + int(TOTAL_MODEL)
        if len(final_shots) < total_target:
            remaining = [x for x in available if x not in final_shots]
            final_shots.extend(remaining[:total_target - len(final_shots)])

    # ── Generate in chunks of 2 to avoid overloading the API ─────────────────
    results_out = []
    chunk_size  = 2
    for i in range(0, len(final_shots), chunk_size):
        chunk = final_shots[i : i + chunk_size]
        chunk_results = await asyncio.gather(*[
            generate_image(client, image_bytes, mime_type, design_lock, s, out_dir, category, worn_on, is_m, session_id)
            for s, is_m in chunk
        ], return_exceptions=True)
        results_out.extend(chunk_results)

    return [r for r in results_out if isinstance(r, dict)]

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
