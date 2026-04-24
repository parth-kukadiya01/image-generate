import os
import asyncio
import mimetypes
import random
from pathlib import Path
from PIL import Image
from google import genai
from google.genai import types

GEMINI_API_KEY = "AIzaSyC4MgiZ_qJD-1ITn78oz6ezKfcgJ4M1shQ"
MODEL          = "gemini-2.5-flash-image" # Correcting to the intended model if approved
TOTAL_PRODUCT  = 2
TOTAL_MODEL    = 2
LOGO_PATH      = "/Users/parthkukadiya/work/pint_automation/riolls_logo.png"

# ── PER-CATEGORY VISUAL IDENTITY SYSTEM ─────────────────────────────────────
CATEGORY_THEMES = {
    "ring": {
        "surface": "honed black Belgian marble with white mineral veins and a near-mirror polish",
        "lighting": "single large diffused panel at 45° left — crisp shadow line across the marble, dramatic stone fire",
        "palette": "obsidian black, cold white metallic flash, deep charcoal",
        "mood": "minimalist jeweler's showcase — architectural precision, the stone as protagonist",
    },
    "necklace": {
        "surface": "raw ivory peau-de-soie silk, naturally draped with visible fabric weave",
        "lighting": "diffused north-facing window light with soft warm fill from the right — Paris atelier morning",
        "palette": "warm ivory, ecru, cream, champagne, sand",
        "mood": "soft couture editorial — feminine, serene, Chanel Fine Jewellery lookbook warmth",
    },
    "bracelet": {
        "surface": "dark oiled walnut wood plank with visible grain lines; raw natural linen strip in foreground",
        "lighting": "warm raking golden light from the right at 30°, long amber shadows along the wood grain",
        "palette": "deep espresso, tobacco brown, raw linen, warm amber, burnished metal",
        "mood": "artisanal atelier — master craftsman's workshop, Florence luxury leather district warmth",
    },
    "earring": {
        "surface": "dusty mauve velvet with directional pile texture; blush suede as secondary accent surface",
        "lighting": "intimate soft north-light from directly above at 15° — velvet absorbs and diffuses, no harsh shadows",
        "palette": "dusty mauve, blush rose, antique ivory, aged gold",
        "mood": "intimate Parisian boutique display — precious, close, high-fashion couture",
    },
    "pendant": {
        "surface": "crisp white textured linen fabric, naturally draped with a visible organic weave",
        "lighting": "bright, soft diffused morning sunlight from a large window — airy and luminous",
        "palette": "pure white, warm off-white, luminous silver, bright airy tones",
        "mood": "clean, modern bridal or high-end minimal luxury — fresh, breathable, and pure",
    },
    "pendant_set": {
        "surface": "crisp white textured linen fabric, naturally draped with a visible organic weave",
        "lighting": "bright, soft diffused morning sunlight from a large window — airy and luminous",
        "palette": "pure white, warm off-white, luminous silver, bright airy tones",
        "mood": "clean, modern bridal or high-end minimal luxury — elegant matching set display",
    },
    "bangle": {
        "surface": "aged mercury mirror with oxidation patina; antique brass tray as secondary accent surface",
        "lighting": "warm afternoon light at 30° from upper left — mirror creates secondary warm reflected light sources",
        "palette": "antique silver, aged gold, champagne, oxidized brass, warm ivory",
        "mood": "high-fashion editorial — Bottega Veneta or Hermès campaign, layered infinite reflections",
    },
    "anklet": {
        "surface": "warm terracotta stone tile alternating with natural fine-grain desert sand",
        "lighting": "warm golden-hour sunlight at low 20° angle — long amber shadows, sun-drenched Mediterranean warmth",
        "palette": "terracotta orange, sandy beige, warm copper, sun-bleached bone, golden amber",
        "mood": "Mediterranean vacation editorial — organic, earthy, aspirational sun-drenched luxury",
    },
    "brooch": {
        "surface": "midnight navy velvet with rich directional pile; aged ivory dupioni silk with visible slub texture",
        "lighting": "Rembrandt-style — single warm source 45° upper left, 70% of frame in deep shadow",
        "palette": "midnight navy, deep emerald, rich burgundy, aged ivory, oxidized gold",
        "mood": "old-world haute couture — Cartier heritage exhibition, Louvre display-case drama",
    },
}


def get_category_theme_block(category: str) -> str:
    """Returns the per-category visual identity block to inject into every prompt."""
    t = CATEGORY_THEMES.get(category, {})
    if not t:
        return ""
    return (
        f"CATEGORY VISUAL IDENTITY — {category.upper()} PHOTOGRAPHY:\n"
        f"- SIGNATURE SURFACE: {t['surface']}\n"
        f"- LIGHTING SETUP: {t['lighting']}\n"
        f"- COLOR PALETTE: {t['palette']}\n"
        f"- EDITORIAL MOOD: {t['mood']}\n"
        "CRITICAL: Use EXACTLY this surface and lighting setup. "
        "Do NOT substitute with white or plain backgrounds. "
        "The background material is a NON-NEGOTIABLE part of the composition.\n"
    )


CATEGORIES = {
    # ── RING ──────────────────────────────────────────────────────────────────
    "ring": {
        "worn_on": "ring finger",
        "product": [
            {
                "key":   "01_product_hero_marble",
                "label": "Product — Hero Upright on Black Marble",
                "shot":  (
                    "The ring standing upright on honed black Belgian marble, shot straight-on at eye level. "
                    "The face of the ring fills the frame symmetrically. Its reflection stretches below on the near-mirror marble surface. "
                    "Single diffused panel light 45° from the left — a crisp shadow line cuts across the marble, revealing stone fire. "
                    "85mm equivalent, f/2.8. Obsidian background. Cartier press-shot quality."
                ),
            },
            {
                "key":   "03_product_topdown_marble",
                "label": "Product — Top-Down on Black Marble",
                "shot":  (
                    "The ring lying flat on honed black Belgian marble, shot from exactly overhead. "
                    "White mineral veins in the marble frame the piece. Soft overhead diffused light. "
                    "The ring's faint reflection is visible on the polished marble. "
                    "Perfect symmetry, 50mm, deep focus. Cold, architectural, precise."
                ),
            },
            {
                "key":   "08_product_dramatic45_marble",
                "label": "Product — Dramatic Low 45° on Black Marble",
                "shot":  (
                    "The ring at a dynamic 45-degree angle on black Belgian marble, camera barely above marble level. "
                    "The shadow stretches dramatically to the right. Single side light — stones explode with fire. "
                    "The reflection in the marble shows the underside of the band. "
                    "35mm, cinematic jeweler's tension."
                ),
            },
            {
                "key":   "09_product_stone_macro_marble",
                "label": "Product — Stone Macro on Black Marble",
                "shot":  (
                    "Extreme macro: the center stone fills 60% of the frame on black Belgian marble. "
                    "Facets are razor-sharp, internal light dispersion visible. "
                    "The dark marble surround lets the stone's color and fire dominate. "
                    "100mm macro, f/2.0, ultra-shallow DoF, marble texture at frame edges."
                ),
            },
        ],
        "model": [
            {
                "key":   "05_model_hand_marble",
                "label": "Model — Hand Resting on Black Marble",
                "shot":  (
                    "A real woman's hand with natural skin texture and visible pores rests on honed black Belgian marble. "
                    "The ring on the ring finger at true natural size (17-19mm). "
                    "The hand's reflection is faintly visible in the marble. Dramatic side light from the left. "
                    "Warm skin against cold obsidian marble — striking contrast. 85mm, f/2.0."
                ),
            },
            {
                "key":   "06_model_hand_raised_dark",
                "label": "Model — Hand Raised Against Dark Background",
                "shot":  (
                    "A real female hand raised gracefully, ring on the ring finger. "
                    "Dark background echoing the black marble palette. Natural skin texture and nude polish. "
                    "Soft single light from the left, ring in perfect focus, hand blurs toward wrist. "
                    "Cinematic mid-palm crop. 85mm, f/1.8. Van Cleef editorial standard."
                ),
            },
            {
                "key":   "12_model_index_marble",
                "label": "Model — Index Finger Close-Up on Marble",
                "shot":  (
                    "Close-up of a real woman's index finger with the ring, finger resting on black Belgian marble. "
                    "Marble texture, skin pores, and ring details all sharp simultaneously. "
                    "Dramatic single side light. The ring's marble reflection visible beneath the finger. "
                    "100mm macro, shallow DoF."
                ),
            },
            {
                "key":   "13_model_cashmere_lifestyle",
                "label": "Model — Hand on Dark Cashmere",
                "shot":  (
                    "A real woman's hand resting on the lapel of a deep charcoal cashmere coat. "
                    "Ring catches natural light against soft cashmere fibers — texture visible and sharp. "
                    "Natural window light from the left. High-end lifestyle editorial. "
                    "Authentic skin details, dark tonal palette consistent with the marble studio."
                ),
            },
        ],
    },


    # ── NECKLACE ──────────────────────────────────────────────────────────────
    "necklace": {
        "worn_on": "neck and collarbone",
        "product": [
            {
                "key":   "01_product_silk_hang",
                "label": "Product — Draped on Ivory Silk",
                "shot":  (
                    "The necklace draped over naturally folded raw ivory peau-de-soie silk, shot straight-on. "
                    "The chain hangs in an organic arc, the pendant resting at the silk fold. "
                    "Diffused north-facing window light — no harsh shadows, soft Paris atelier morning. "
                    "The visible silk weave texture contrasts richly against the metal chain. 85mm, f/2.8."
                ),
            },
            {
                "key":   "02_product_flat_silk",
                "label": "Product — Flat Lay on Ivory Silk",
                "shot":  (
                    "The necklace laid flat on raw ivory silk fabric, shot from directly overhead. "
                    "Chain in a gentle open arc. The silk weave is fully visible, catching soft diffused north light. "
                    "Warm ivory palette makes the metal glow naturally. 50mm, f/4. "
                    "Organic shadows where chain rests on the silk."
                ),
            },
            {
                "key":   "03_product_pendant_silk_macro",
                "label": "Product — Pendant Macro on Ivory Silk",
                "shot":  (
                    "Extreme macro of the pendant resting directly on raw ivory peau-de-soie silk. "
                    "The silk weave is sharp and visible beneath the stone — rich textile texture contrast. "
                    "Soft diffused north light. Pendant fills most of frame. "
                    "100mm macro, f/2.0, ultra-shallow DoF with creamy silk bokeh at edges."
                ),
            },
            {
                "key":   "04_product_couture_45",
                "label": "Product — Couture 45° Angle on Silk",
                "shot":  (
                    "The necklace hanging at a 45-degree glamour angle, draped ivory silk as backdrop. "
                    "Warm right-side fill light creates a subtle glow on the fabric. "
                    "Pendant catches diffused light, depth clearly visible. "
                    "85mm, f/2.0, soft silk bokeh background. Chanel Fine Jewellery lookbook quality."
                ),
            },
        ],
        "model": [
            {
                "key":   "05_model_collarbone_silk",
                "label": "Model — Collarbone on Ivory Silk Blouse",
                "shot":  (
                    "Editorial portrait of a real woman's collarbone and neck. "
                    "She wears a raw ivory silk blouse; the necklace rests on bare skin at the collar. "
                    "True scale (pendant 15-30mm). Diffused north window light, skin texture and pores sharp. "
                    "Softly out-of-focus ivory fabric background. 85mm, f/2.0. Vogue editorial standard."
                ),
            },
            {
                "key":   "06_model_pendant_skin_macro",
                "label": "Model — Pendant Macro on Bare Skin",
                "shot":  (
                    "Extreme macro: pendant on a real woman's bare collarbone. "
                    "Skin pores, warmth, and the natural rise of the collarbone sharp and visible. "
                    "Pendant at true delicate scale. Diffused warm window light. "
                    "Razor-thin DoF, ivory silk bokeh background. Authentic luxury editorial."
                ),
            },
            {
                "key":   "09_model_ivory_lifestyle",
                "label": "Model — Over Ivory Silk Top Lifestyle",
                "shot":  (
                    "A real woman wearing the necklace over an ivory or ecru silk blouse. "
                    "Necklace at natural scale; silk fabric texture visible and sharp. "
                    "Natural window light from left, soft warm fill from right. "
                    "Paris atelier morning atmosphere — refined, quiet luxury."
                ),
            },
            {
                "key":   "12_model_neck_profile_ivory",
                "label": "Model — Neck Side Profile, Ivory Backdrop",
                "shot":  (
                    "A real woman's neck in side profile. Chain wraps neck naturally, pendant visible at front. "
                    "Ivory silk fabric softly blurred behind. "
                    "Natural north light, sharp skin detail on neck, organic shadow on the far side. "
                    "Shallow DoF, authentic luxury editorial."
                ),
            },
        ],
    },


    # ── BRACELET ──────────────────────────────────────────────────────────────
    "bracelet": {
        "worn_on": "wrist",
        "product": [
            {
                "key":   "01_product_walnut_upright",
                "label": "Product — Upright on Dark Walnut",
                "shot":  (
                    "The bracelet standing upright on a dark oiled walnut wood plank, grain lines running left to right. "
                    "A strip of raw natural linen fabric visible in the foreground. "
                    "Warm raking golden light from the right at 30° casts long amber shadows along the wood grain. "
                    "Jewelry brilliance against organic warm wood. 85mm, f/2.8."
                ),
            },
            {
                "key":   "02_product_walnut_45",
                "label": "Product — Glamour 45° on Walnut",
                "shot":  (
                    "The bracelet at a 45-degree angle on dark oiled walnut, camera at a low angle. "
                    "Warm golden side light from the right illuminates the stones. "
                    "Walnut grain creates natural leading lines toward the piece. "
                    "Raw linen softens the background. 35mm, f/2.0, warm amber tones throughout."
                ),
            },
            {
                "key":   "03_product_linen_topdown",
                "label": "Product — Flat on Raw Linen Top-Down",
                "shot":  (
                    "The bracelet lying flat on raw natural linen fabric, shot from directly above. "
                    "The linen weave texture fully visible around the piece. "
                    "Warm raking side light creates subtle shadows in the linen weave. "
                    "50mm, f/4. Warm palette — linen, tobacco, burnished metal."
                ),
            },
            {
                "key":   "04_product_clasp_walnut",
                "label": "Product — Clasp Detail on Walnut",
                "shot":  (
                    "Close-up of the bracelet clasp on dark walnut. "
                    "Shows craftsmanship and closure mechanism in precise detail. "
                    "Warm golden light from the right. Walnut grain runs beside the clasp, adding texture. "
                    "100mm macro, f/2.8, razor-sharp focus on mechanism."
                ),
            },
        ],
        "model": [
            {
                "key":   "05_model_wrist_walnut",
                "label": "Model — Wrist Resting on Dark Walnut",
                "shot":  (
                    "A real female wrist with natural skin tone and visible pores, resting on the dark walnut plank. "
                    "Bracelet at correct natural size. Walnut grain and skin warmth create a rich organic composition. "
                    "Warm golden side light from the right. 85mm, f/2.0. "
                    "Indistinguishable from a luxury brand campaign photograph."
                ),
            },
            {
                "key":   "06_model_wrist_linen",
                "label": "Model — Wrist on Raw Linen Lifestyle",
                "shot":  (
                    "A real woman's wrist resting on raw natural linen fabric. "
                    "Bracelet at natural size, linen weave texture visible beneath. "
                    "Warm directional natural light. Artisan, handcrafted warmth. "
                    "Shallow DoF, genuine proportions, photorealistic."
                ),
            },
            {
                "key":   "09_model_silk_cuff",
                "label": "Model — Bracelet Over Silk Cuff",
                "shot":  (
                    "The bracelet worn over the cuff of a high-end ivory silk blouse on a real woman's wrist. "
                    "Natural window light from the left, silk fabric texture and bracelet both sharp. "
                    "Authentic lifestyle editorial quality."
                ),
            },
        ],
    },


    # ── EARRING ───────────────────────────────────────────────────────────────
    "earring": {
        "worn_on": "earlobe",
        "product": [
            {
                "key":   "01_product_velvet_pair",
                "label": "Product — Pair on Dusty Mauve Velvet",
                "shot":  (
                    "Both earrings as a matching pair on dusty mauve velvet, directional pile texture visible. "
                    "Side by side, precisely spaced. Intimate soft north-light from above at 15°. "
                    "Velvet absorbs light around the pieces, creating a dark surround that makes stones pop. "
                    "85mm, f/2.8. Parisian boutique display quality."
                ),
            },
            {
                "key":   "02_product_velvet_single45",
                "label": "Product — Single Earring 45° on Velvet",
                "shot":  (
                    "One earring propped at a 45-degree angle on the dusty mauve velvet surface. "
                    "Velvet pile direction creates subtle texture leading to the piece. "
                    "Soft north-light from above. Stones catch light naturally, no artificial sparkle. "
                    "85mm, f/2.0. Blush suede visible in soft focus behind."
                ),
            },
            {
                "key":   "03_product_velvet_topdown",
                "label": "Product — Pair Top-Down on Velvet",
                "shot":  (
                    "Both earrings laid flat on dusty mauve velvet, shot from directly above. "
                    "Symmetrically placed. Even velvet pile sheen creates tactile depth. "
                    "Soft overhead north-light. 50mm, f/4, even illumination."
                ),
            },
            {
                "key":   "04_product_suede_side",
                "label": "Product — Single Side Profile on Blush Suede",
                "shot":  (
                    "One earring at a 90-degree side profile, placed on blush suede fabric. "
                    "Shows depth, backing, and stud or hook mechanism. "
                    "Suede surface texture warm and soft in frame. "
                    "Soft north-light, 100mm macro, f/2.8, velvet in background bokeh."
                ),
            },
        ],
        "model": [
            {
                "key":   "05_model_ear_velvet_bg",
                "label": "Model — Ear Side Profile, Velvet Backdrop",
                "shot":  (
                    "A real woman's ear in side profile, earring at its precise natural size. "
                    "Dusty mauve velvet softly blurred in the background — rich tonal surround. "
                    "Soft north-light: skin texture, pores, natural warmth all visible. "
                    "Earring razor-sharp in focus. 85mm, f/2.0. Intimate luxury editorial."
                ),
            },
            {
                "key":   "06_model_face_34_suede",
                "label": "Model — Face 3/4 Angle, Suede Background",
                "shot":  (
                    "Three-quarter portrait of a real woman. Earring in perfect proportion — small, refined. "
                    "Blush suede creates a warm, soft backdrop. "
                    "Natural window light, subtle bokeh. Photorealistic skin and hair texture. "
                    "Earring catches side light naturally."
                ),
            },
            {
                "key":   "09_model_hair_lifestyle",
                "label": "Model — Hair Behind Ear Lifestyle",
                "shot":  (
                    "A real woman's profile as her hand brushes hair behind her ear, revealing the earring. "
                    "Earring catches light at the perfect moment. Realistic skin and proportions. "
                    "Blush suede and velvet tones in the background bokeh. Cinematic, lifestyle atmosphere."
                ),
            },
            {
                "key":   "12_model_ear_macro_skin",
                "label": "Model — Extreme Ear Macro",
                "shot":  (
                    "Extreme macro of the earring on a real woman's earlobe. "
                    "Razor-sharp stones, natural skin pores and texture visible at macro distance. "
                    "Soft north-light, dusty mauve background bokeh. Authentic luxury editorial."
                ),
            },
        ],
    },


    # ── PENDANT ───────────────────────────────────────────────────────────────
    "pendant": {
        "worn_on": "neck (on a chain)",
        "product": [
            {
                "key":   "01_product_linen_front",
                "label": "Product — Pendant Front on White Linen",
                "shot":  (
                    "The pendant alone on crisp white textured linen fabric, shot straight-on. "
                    "Organic weave of the linen visible beside the piece. "
                    "Bright, soft diffused morning sunlight from a large window. "
                    "All pendant details sharp. Luminous, airy luxury."
                ),
            },
            {
                "key":   "02_product_linen_45",
                "label": "Product — Pendant Glamour 45° on Linen",
                "shot":  (
                    "The pendant hanging on its chain against draped white linen fabric at 45 degrees. "
                    "Soft morning light creates subtle, airy shadows in the fabric folds. "
                    "Luminous white palette frames the piece. 85mm, f/2.0."
                ),
            },
            {
                "key":   "03_product_linen_topdown",
                "label": "Product — Top-Down on White Linen",
                "shot":  (
                    "The pendant lying flat on white textured linen, shot from directly above. "
                    "Linen weave visible throughout. Bright, soft diffused overhead light. "
                    "Fresh, modern bridal luxury. 50mm, f/4, sharp focus across the piece."
                ),
            },
            {
                "key":   "04_product_linen_back",
                "label": "Product — Back Detail on Linen",
                "shot":  (
                    "The back of the pendant shown clearly on the white linen surface. "
                    "Shows engravings and bail attachment. Bright airy light, sharp focus. "
                    "Matte white linen backdrop creates a clean, elegant quality."
                ),
            },
        ],
        "model": [
            {
                "key":   "05_model_collarbone_linen",
                "label": "Model — Pendant on Collarbone, White Linen Blouse",
                "shot":  (
                    "Editorial portrait of a real woman wearing the pendant with a white linen blouse. "
                    "Pendant at true-to-life size (15-30mm) on bare skin. "
                    "Luminous white background echoing the clean palette. "
                    "Soft diffused morning light, natural skin texture visible."
                ),
            },
            {
                "key":   "06_model_pendant_skin_macro",
                "label": "Model — Pendant Macro on Skin",
                "shot":  (
                    "Macro close-up of the pendant on a real woman's bare skin. "
                    "True, delicate scale. Soft morning light catching stone facets. "
                    "Razor shallow DoF, luminous bright bokeh background. Refined bridal luxury."
                ),
            },
            {
                "key":   "09_model_lifestyle_holding",
                "label": "Model — Hand Touching Pendant",
                "shot":  (
                    "A real woman's hand gently touching the pendant while wearing it. "
                    "Bright window light, realistic skin and nail texture. "
                    "Clean, airy tones. Authentic high-end lifestyle photography."
                ),
            },
        ],
    },

    # ── PENDANT SET (PENDANT + EARRINGS) ──────────────────────────────────────
    "pendant_set": {
        "worn_on": "neck and earlobes",
        "product": [
            {
                "key":   "01_product_set_front",
                "label": "Product — Set Front on White Linen",
                "shot":  (
                    "The pendant and matching earrings laid together on crisp white textured linen fabric. "
                    "Organized beautifully, shot straight-on. Organic weave of the linen visible. "
                    "Bright, soft diffused morning sunlight from a large window. "
                    "All details sharp. Luminous, airy luxury."
                ),
            },
            {
                "key":   "02_product_set_45",
                "label": "Product — Set Glamour 45° on Linen",
                "shot":  (
                    "The pendant and earrings arranged artistically against draped white linen fabric at 45 degrees. "
                    "Soft morning light creates subtle, airy shadows in the fabric folds. "
                    "Luminous white palette frames the matching pieces. 85mm, f/2.0."
                ),
            },
            {
                "key":   "03_product_set_topdown",
                "label": "Product — Top-Down Set on White Linen",
                "shot":  (
                    "The pendant and matching earrings lying flat on white textured linen, shot from directly above. "
                    "Symmetrically placed. Linen weave visible throughout. Bright, soft diffused overhead light. "
                    "Fresh, modern bridal luxury. 50mm, f/4, sharp focus across all pieces."
                ),
            },
        ],
        "model": [
            {
                "key":   "05_model_set_worn",
                "label": "Model — Wearing Set, White Linen Blouse",
                "shot":  (
                    "Editorial portrait of a real woman wearing both the pendant and matching earrings. "
                    "Pieces at true-to-life size. She wears a white linen blouse. "
                    "Luminous white background. Soft diffused morning light, natural skin texture visible."
                ),
            },
            {
                "key":   "06_model_set_macro",
                "label": "Model — Set Detail on Skin",
                "shot":  (
                    "Close-up highlighting either the pendant or earring on a real woman's skin, "
                    "with the other matching piece softly visible in the background bokeh. "
                    "True scale. Soft morning light. Razor shallow DoF, luminous bright background."
                ),
            },
        ],
    },


    # ── BANGLE ────────────────────────────────────────────────────────────────
    "bangle": {
        "worn_on": "wrist",
        "product": [
            {
                "key":   "01_product_mirror_upright",
                "label": "Product — Upright on Antique Mirror",
                "shot":  (
                    "The bangle standing upright on an aged mercury mirror surface with visible oxidation patina. "
                    "The bangle's reflection in the mirror creates an infinite-depth editorial effect. "
                    "Warm afternoon light at 30° from upper left — mirror creates secondary warm reflections. "
                    "Antique silver and aged gold tones. 85mm, f/2.8."
                ),
            },
            {
                "key":   "03_product_mirror_45",
                "label": "Product — Glamour 45° on Antique Mirror",
                "shot":  (
                    "The bangle at a 45-degree angle on the aged mercury mirror. "
                    "Low camera angle — the mirror's reflection doubles the piece beneath it. "
                    "Warm afternoon light from upper left. Antique brass tray visible in background. "
                    "Stones and depth clearly visible. 35mm, f/2.0, champagne and oxidized tones."
                ),
            },
            {
                "key":   "02_product_brass_topdown",
                "label": "Product — Top-Down on Antique Brass Tray",
                "shot":  (
                    "The bangle lying flat on an antique brass tray, shot from directly above. "
                    "Warm brass surface texture visible around the piece. "
                    "Warm afternoon light from the side. Oxidized gold tones, warm ivory accents. "
                    "50mm, f/4, sharp focus on stones."
                ),
            },
            {
                "key":   "04_product_mirror_side",
                "label": "Product — Side Profile on Mirror",
                "shot":  (
                    "The bangle standing upright on the aged mercury mirror, 90-degree side profile. "
                    "Shows width, stone arrangement, and its mirror reflection below. "
                    "Warm directional light. Bottega Veneta campaign quality."
                ),
            },
        ],
        "model": [
            {
                "key":   "05_model_wrist_mirror",
                "label": "Model — Wrist Reflected on Antique Mirror",
                "shot":  (
                    "A real female wrist wearing the bangle at natural size, resting on or near the aged mercury mirror. "
                    "The wrist and bangle are reflected in the mirror surface. "
                    "Warm afternoon light. Natural skin texture, antique silver and gold tones. "
                    "85mm, f/2.0. Hermès campaign quality."
                ),
            },
            {
                "key":   "06_model_wrist_brass",
                "label": "Model — Wrist Lifestyle, Warm Brass Tones",
                "shot":  (
                    "A relaxed lifestyle shot of a real woman's wrist wearing the bangle. "
                    "Warm antique brass and aged gold tones in the background. "
                    "Natural warm light source. Sharp focus on the bangle, genuine proportions."
                ),
            },
            {
                "key":   "09_model_stacked_mirror",
                "label": "Model — Stacked with Watch on Mirror Surface",
                "shot":  (
                    "The bangle worn alongside a delicate vintage watch on a real woman's wrist. "
                    "Fashion-forward, editorial luxury. Aged mirror surface in the background. "
                    "Warm afternoon light, authentic tones."
                ),
            },
        ],
    },


    # ── ANKLET ────────────────────────────────────────────────────────────────
    "anklet": {
        "worn_on": "ankle",
        "product": [
            {
                "key":   "01_product_sand_flatlay",
                "label": "Product — Flat Lay on Desert Sand",
                "shot":  (
                    "The anklet laid flat on natural fine-grain desert sand, shot from directly above. "
                    "Sand texture fully visible, warm golden-hour light from low 20° angle. "
                    "Long warm shadows in the sand beside the piece. "
                    "Terracotta and sandy beige tones. 50mm, f/4."
                ),
            },
            {
                "key":   "02_product_terracotta_45",
                "label": "Product — Glamour 45° on Terracotta Stone",
                "shot":  (
                    "The anklet draped at a 45-degree angle on warm terracotta stone tile. "
                    "Golden-hour sun from a low angle — long amber shadows, stone texture visible. "
                    "Mediterranean vacation atmosphere. 85mm, f/2.0."
                ),
            },
            {
                "key":   "03_product_terracotta_hang",
                "label": "Product — Hanging Against Terracotta Wall",
                "shot":  (
                    "The anklet hanging vertically against a warm terracotta stone surface. "
                    "Full length of chain visible. Golden-hour warm light from the side. "
                    "Terracotta orange and sun-bleached bone tones. Authentic Mediterranean."
                ),
            },
            {
                "key":   "04_product_charm_sand_macro",
                "label": "Product — Charm Macro on Sand",
                "shot":  (
                    "Close-up macro of charms or stones resting directly on fine desert sand. "
                    "Sand grains visible at macro distance around the piece. "
                    "Warm golden-hour light. Razor-thin DoF, warm copper and sandy tones."
                ),
            },
        ],
        "model": [
            {
                "key":   "05_model_ankle_terracotta",
                "label": "Model — Ankle on Terracotta Stone",
                "shot":  (
                    "A real woman's ankle resting on warm terracotta stone tile. "
                    "Anklet at its true natural size. Golden-hour light, long warm shadows. "
                    "Real skin texture, warm copper tones. Sharp focus on the jewelry."
                ),
            },
            {
                "key":   "06_model_ankle_sand",
                "label": "Model — Ankle in Desert Sand",
                "shot":  (
                    "A real woman's ankle resting in fine desert sand. "
                    "Anklet at natural size, sand grains visible on skin. "
                    "Warm golden-hour light at a low angle. Sandy beige and warm copper tones. "
                    "Authentic Mediterranean editorial."
                ),
            },
            {
                "key":   "09_model_goldhour_lifestyle",
                "label": "Model — Golden Hour Vacation Lifestyle",
                "shot":  (
                    "A real woman's ankle with the anklet, bathed in golden-hour sunlight on terracotta. "
                    "The warm amber light creates long shadows across the stone tile. "
                    "Skin texture sharp and warm. Aspirational sun-drenched luxury vacation aesthetic."
                ),
            },
        ],
    },


    # ── BROOCH ────────────────────────────────────────────────────────────────
    "brooch": {
        "worn_on": "chest or lapel",
        "product": [
            {
                "key":   "01_product_velvet_topdown",
                "label": "Product — Hero Top-Down on Midnight Navy Velvet",
                "shot":  (
                    "The brooch flat on midnight navy velvet, shot from directly above. "
                    "All stones visible against the deep navy pile. "
                    "Rembrandt-style single warm source at 45° upper left — 70% of frame in deep shadow. "
                    "The stones erupt with brilliance from the dark surround. Cartier heritage quality."
                ),
            },
            {
                "key":   "02_product_silk_45",
                "label": "Product — Glamour 45° on Aged Ivory Silk",
                "shot":  (
                    "The brooch propped on aged ivory dupioni silk with visible slub texture, shot from 45 degrees. "
                    "Rembrandt warm light from upper left — dramatic shadow on the right half. "
                    "Deep contrast between ivory silk and brooch. Haute couture editorial."
                ),
            },
            {
                "key":   "03_product_velvet_side",
                "label": "Product — Side Profile on Navy Velvet",
                "shot":  (
                    "The brooch at a 90-degree side profile on midnight navy velvet. "
                    "Shows pin mechanism in shadow. Single warm Rembrandt light from upper left. "
                    "Rich dramatic depth. Louvre display-case quality."
                ),
            },
            {
                "key":   "04_product_velvet_stone_macro",
                "label": "Product — Stone Macro on Navy Velvet",
                "shot":  (
                    "Extreme macro of the brooch stones against midnight navy velvet pile. "
                    "Velvet pile visible at macro scale around the stones. "
                    "Rembrandt warm light — stones burst with fire against deep dark background. "
                    "100mm macro, ultra-shallow DoF, razor-sharp facets."
                ),
            },
        ],
        "model": [
            {
                "key":   "05_model_velvet_lapel",
                "label": "Model — Lapel on Midnight Navy Blazer",
                "shot":  (
                    "A real woman wearing the brooch on the lapel of a midnight navy wool blazer. "
                    "Brooch at true-to-life scale against the dark fabric. "
                    "Rembrandt-style light from upper left — dramatic shadow on the right. "
                    "Fabric weave visible and sharp. Old-world haute couture quality."
                ),
            },
            {
                "key":   "06_model_silk_lapel_close",
                "label": "Model — Brooch Close-Up on Ivory Silk Lapel",
                "shot":  (
                    "Editorial close-up of the brooch on a real woman's aged ivory silk lapel. "
                    "Silk slub texture sharp around the piece. "
                    "Warm Rembrandt light, organic shadow. Deep luxury brand quality."
                ),
            },
            {
                "key":   "09_model_navy_scarf",
                "label": "Model — Brooch on Navy or Burgundy Scarf",
                "shot":  (
                    "The brooch pinned to a rich navy or deep burgundy scarf worn by a real woman. "
                    "Rembrandt warm light from upper left. Dramatic fabric texture visible. "
                    "Midnight navy palette, authentic old-world luxury feel."
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
    "pendant set": "pendant_set", "pendant sets": "pendant_set",
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
    theme_context = get_category_theme_block(category)
    resp = await client.aio.models.generate_content(
        model=MODEL,
        contents=[
            types.Part.from_bytes(data=img, mime_type=mime),
            types.Part.from_text(text=f"""
You are analyzing a {category} for a premium 2026 editorial jewelry shoot.
The final images will be shot in the following visual style:
{theme_context}

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
Select exactly {int(TOTAL_PRODUCT)} Product shots and {int(TOTAL_MODEL)} Model shots from the list above
that would best showcase this design given the editorial style described above.
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
"""

ANGLE_RULES = """
CRITICAL ANGLE AND SURFACE OVERRIDE:
- You MUST completely ignore the camera angle from the provided reference image!
- The reference image is ONLY for learning the design (stones, metal, shape).
- Do NOT generate the same angle as the reference image under any circumstances!
- You MUST render the jewelry from the EXACT angle described in the "CAMERA ANGLE / SHOT COMPOSITION" section.
- If the instruction says "Top-Down", render it perfectly flat from above.
- If the instruction says "Macro Close-Up", zoom in directly.
- The angle is the absolute most important requirement. Repeating the same angle is a severe failure.

SURFACE OVERRIDE RULE:
- The CATEGORY VISUAL IDENTITY surface and lighting ALWAYS takes priority.
- If the shot description mentions a different surface (e.g. "marble", "stone"), IGNORE it.
- Use ONLY the signature surface and lighting defined in the CATEGORY VISUAL IDENTITY block.
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
STRICT PROFESSIONAL JEWELRY PHOTOGRAPHY RULES — 2026 PREMIUM STANDARD:
1. RAW PHOTOGRAPHY STYLE: Must look like a Phase One IQ4 or Hasselblad X2D photograph shot by a master jewelry photographer. Zero AI glow, zero plastic surfaces, zero CGI look.
2. CATEGORY SURFACE MANDATORY: Use EXACTLY the surface material defined in the CATEGORY VISUAL IDENTITY block. NEVER substitute with white or plain backgrounds.
3. AUTHENTIC METAL TEXTURE: Metal must show microscopic surface texture, subtle micro-reflections, genuine polish — NOT liquid-smooth or mirror-perfect.
4. BACKGROUND DEPTH AND GRAIN: The background surface must show tactile depth — grain, weave, veining, or pile — never a flat tone.
5. REAL DEPTH OF FIELD & FOCUS STACKING: The jewelry piece itself must be razor-sharp (simulating focus stacking), while the background falls into a natural, creamy bokeh.
6. PROFESSIONAL LIGHTING MODIFIERS: Simulate the use of high-end studio modifiers. Use negative fill to create sharp contrast in diamonds, and precise bounce cards to create clean, elegant highlights on the metal.
7. FILM COLOR GRADING: Natural, muted, organic tones matching the category palette. No oversaturation, no neon, no digital color casts.
8. SUBTLE GRAIN: A fine photographic grain is acceptable and desirable — it signals a real photograph, not a render.
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

{get_category_theme_block(category)}
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
- Real human skin: natural texture, pores, warmth — NOT plastic or AI-smooth.
- Natural lighting matching the CATEGORY VISUAL IDENTITY above. Organic shadows are mandatory.
- The jewelry must match the reference image design exactly. No extra stones, no missing pieces.
- The overall image must be photorealistic and indistinguishable from a real luxury editorial photograph.
"""
    else:
        prompt = f"""
You are a 2026 premium jewelry photographer generating an editorial product shot.

JEWELRY PIECE ({category}):
{design_lock}

Study the design description above and the reference image carefully.

{DESIGN_LOCK_RULES}

{get_category_theme_block(category)}
{PHOTOGRAPHY_REALISM_RULES}

{ANGLE_RULES}

CAMERA ANGLE / SHOT COMPOSITION:
{shot['shot']}
THIS CAMERA ANGLE IS MANDATORY. RENDER THIS PRECISE PERSPECTIVE.

PRODUCT SHOT RULES:
- Use EXACTLY the surface and lighting defined in CATEGORY VISUAL IDENTITY above — this is mandatory.
- The background must show grain, texture, and depth — NEVER flat, NEVER plain white.
- Photorealistic quality, razor-sharp focus on the jewelry, organic depth of field.
- The jewelry must match the reference image exactly. No extra stones, no missing pieces.
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
        keywords = ["front", "side", "top", "macro", "profile", "hand"]
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

    # Process 2 shots at a time to prevent server overload / rate limits
    final_results = []
    chunk_size = 2
    for i in range(0, len(selected_shots), chunk_size):
        chunk = selected_shots[i : i + chunk_size]
        chunk_results = await asyncio.gather(*[
            generate_image(client, image_bytes, mime_type, design_lock, s, out_dir, category, worn_on, is_m, session_id)
            for s, is_m in chunk
        ], return_exceptions=True)
        final_results.extend(chunk_results)
        
        if i + chunk_size < len(selected_shots):
            print("Waiting 15 seconds before next chunk to avoid Gemini API rate limits...")
            await asyncio.sleep(15)

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
        
        if i + chunk_size < len(selected_shots):
            print("Waiting 15 seconds before next chunk to avoid Gemini API rate limits...")
            await asyncio.sleep(15)

    return [r for r in final_results if isinstance(r, dict)]
