"""
prompt_config.py
────────────────
Contains all the core prompt structures, scene dictionaries, and mapping rules
for the jewelry generation platform. Abstracted from the generation logic
to allow scaling the project easily.
"""

GLOBAL_THEME_RULES = """
BRAND VISUAL IDENTITY (THEME):
- BACKGROUND: Use a high-end, textured "Creamy Marble" or luxury natural light stone surface for all product shots.
- LIGHTING: Soft, directional natural side-window lighting that creates elegant shadows and emphasizes metal texture.
- AESTHETIC: Quiet luxury, minimalist, and sophisticated.
- DO NOT use different backgrounds or inconsistent lighting across shots.
"""

# Reconstructed 30+ Creative Scenes for the UI Dropdown
CREATIVE_SCENES = [
    {
        "key": "social_01_books",
        "label": "Creative — Antique Books",
        "shot": "The jewelry placed gracefully on an open antique book with slightly yellowed pages. Soft, natural light illuminating the piece.",
        "is_model": False
    },
    {
        "key": "social_02_white_coral",
        "label": "Creative — White Coral",
        "shot": "The jewelry resting on a piece of white sea coral. Organic, beach-inspired luxury aesthetic. Bright, crisp natural light.",
        "is_model": False
    },
    {
        "key": "social_03_champagne",
        "label": "Creative — Champagne Glass",
        "shot": "The jewelry draped on or sitting next to a crystal champagne coupe glass. Elegant, celebratory luxury atmosphere.",
        "is_model": False
    },
    {
        "key": "social_04_minimal_stack",
        "label": "Creative — Minimalist Stack",
        "shot": "The jewelry placed on a minimalist stack of high-end fashion magazines or art books. Modern, clean aesthetic.",
        "is_model": False
    },
    {
        "key": "social_05_silk_sheets",
        "label": "Creative — Silk Sheets",
        "shot": "The jewelry resting softly on unmade, luxurious white silk bed sheets. Intimate, morning light aesthetic.",
        "is_model": False
    },
    {
        "key": "social_06_coffee_cup",
        "label": "Creative — Morning Coffee",
        "shot": "A high-end lifestyle shot of the jewelry placed on a saucer next to an elegant ceramic coffee cup. Warm morning light.",
        "is_model": False
    },
    {
        "key": "social_07_marble_pedestal",
        "label": "Creative — Marble Pedestal",
        "shot": "The jewelry displayed on a sleek, geometric marble pedestal. Museum-like, high-fashion presentation.",
        "is_model": False
    },
    {
        "key": "social_08_flower_petals",
        "label": "Creative — Rose Petals",
        "shot": "The jewelry resting among scattered, fresh white rose petals. Romantic, soft, and elegant.",
        "is_model": False
    },
    {
        "key": "social_09_champagne_confetti",
        "label": "Creative — Celebration Confetti",
        "shot": "The jewelry placed among subtle, golden celebration confetti on a dark surface. Festive luxury.",
        "is_model": False
    },
    {
        "key": "social_10_red_ginger_flower",
        "label": "Creative — Exotic Flora",
        "shot": "The jewelry resting on or near a vibrant red tropical ginger flower. High contrast, exotic aesthetic.",
        "is_model": False
    },
    {
        "key": "social_11_velvet_box",
        "label": "Creative — Velvet Box",
        "shot": "The jewelry inside an open, premium black velvet ring box. Classic, timeless presentation.",
        "is_model": False
    },
    {
        "key": "social_12_sunlight_shadows",
        "label": "Creative — Harsh Sunlight & Shadows",
        "shot": "The jewelry placed on a plain surface with harsh, dramatic sunlight creating strong geometric shadows (like a window blind shadow).",
        "is_model": False
    },
    {
        "key": "social_13_dark_slate",
        "label": "Creative — Dark Slate",
        "shot": "The jewelry on a rough, dark grey slate stone. Moody, masculine, and dramatic contrast.",
        "is_model": False
    },
    {
        "key": "social_14_beige_sand",
        "label": "Creative — Desert Sand",
        "shot": "The jewelry placed on fine, beige desert sand with rippled wind textures. Warm, organic.",
        "is_model": False
    },
    {
        "key": "social_15_blue_pillar",
        "label": "Creative — Blue Geometric Pillar",
        "shot": "The jewelry on a striking cobalt blue geometric pillar or block. Modern art aesthetic.",
        "is_model": False
    },
    {
        "key": "social_16_ice_block",
        "label": "Creative — Frozen Ice",
        "shot": "The jewelry partially submerged or resting on a block of clear ice. Crisp, brilliant, and pure.",
        "is_model": False
    },
    {
        "key": "social_17_mirror_reflection",
        "label": "Creative — Mirror Surface",
        "shot": "The jewelry placed on a mirror surface, reflecting perfectly. Sleek and mesmerizing.",
        "is_model": False
    },
    {
        "key": "social_18_stone_slabs",
        "label": "Creative — Stone Slabs",
        "shot": "The jewelry resting on stacked, raw stone slabs. Earthy, grounded luxury.",
        "is_model": False
    },
    {
        "key": "social_19_water_drops",
        "label": "Creative — Water Drops",
        "shot": "The jewelry on a waterproof dark surface with perfect, distinct water droplets surrounding it. Fresh and clean.",
        "is_model": False
    },
    {
        "key": "social_20_smooth_beige",
        "label": "Creative — Smooth Beige Seamless",
        "shot": "The jewelry on a perfectly smooth, seamless beige background with extremely soft gradient lighting.",
        "is_model": False
    },
    {
        "key": "social_21_vibrant_pink",
        "label": "Creative — Vibrant Pink",
        "shot": "The jewelry on a vibrant, punchy pink background. Bold, youthful, fashion-forward.",
        "is_model": False
    },
    {
        "key": "social_22_dark_mossy_wood",
        "label": "Creative — Dark Wood & Moss",
        "shot": "The jewelry on aged, dark wood with small accents of forest moss. Enchanted, natural.",
        "is_model": False
    },
    {
        "key": "social_23_vogue_close_up",
        "label": "Creative — Vogue Close-up",
        "shot": "Extreme macro close-up of the jewelry with dramatic, high-fashion lighting. Every facet sparkles intensely.",
        "is_model": False
    },
    {
        "key": "social_24_golden_hour_riviera",
        "label": "Creative — Riviera Golden Hour",
        "shot": "The jewelry bathed in warm, golden-hour sunlight as if on a balcony overlooking the French Riviera.",
        "is_model": False
    },
    {
        "key": "social_25_silk_and_shadows",
        "label": "Creative — Silk & Shadows",
        "shot": "The jewelry resting on black silk with moody, dramatic shadows. Sensual and mysterious.",
        "is_model": False
    },
    {
        "key": "social_26_red_carpet_flash",
        "label": "Creative — Red Carpet Flash",
        "shot": "The jewelry illuminated by a harsh, direct paparazzi-style flash against a dark background.",
        "is_model": False
    },
    {
        "key": "social_27_water_reflections",
        "label": "Creative — Aquatic Reflections",
        "shot": "Avant-garde editorial photograph. The jewelry piece with shimmering caustic water reflections cast across the surface. Cool, sophisticated blue-toned lighting.",
        "is_model": False
    },
    {
        "key": "social_28_monochrome_elegance",
        "label": "Studio — Monochrome Elegance",
        "shot": "Premium luxury jewelry studio photography. The model (skin, hair, and clothing) is shot in crisp, high-contrast black-and-white, wearing an elegant black blazer. The background is a soft, warm beige textured surface (NOT black and white). CRITICAL MANDATE: THE JEWELRY ITSELF MUST NOT BE BLACK AND WHITE. The jewelry MUST be in full, highly saturated, true original color, creating a striking selective-color contrast against the monochrome model and warm background. Editorial luxury campaign style.",
        "is_model": True
    },
    {
        "key": "social_29_monochrome_noir",
        "label": "Studio — Monochrome Silhouette",
        "shot": "Ultra-premium jewelry studio photography. The model is shot in a stark, elegant black-and-white silhouette against a crisp studio grey seamless background. CRITICAL MANDATE: THE JEWELRY ITSELF MUST NOT BE BLACK AND WHITE. The jewelry MUST be fully illuminated by a dedicated studio spotlight in striking, vibrant true full color. Bvlgari editorial style.",
        "is_model": True
    },
    {
        "key": "social_30_monochrome_hollywood",
        "label": "Studio — Old Hollywood Monochrome",
        "shot": "Classic 1950s Old Hollywood style portrait photography. A model in glamorous black-and-white (soft glowing skin, deep shadows, vintage elegance). CRITICAL MANDATE: THE JEWELRY ITSELF MUST NOT BE BLACK AND WHITE. The entire scene is monochrome EXCEPT the jewelry, which is rendered in exquisite, photorealistic full true color.",
        "is_model": True
    },
    {
        "key": "social_31_monochrome_satin",
        "label": "Studio — Monochrome Satin",
        "shot": "Modern luxury studio photography. A model draped in black studio satin, photographed in highly detailed black-and-white. Crisp, clean commercial lighting. CRITICAL MANDATE: THE JEWELRY ITSELF MUST NOT BE BLACK AND WHITE. The entire scene is black-and-white EXCEPT the jewelry, which stands out brilliantly in full, exact color. Chopard campaign aesthetic.",
        "is_model": True
    },
    {
        "key": "social_32_linen_fabric",
        "label": "Creative — Linen Fabric",
        "shot": "The exact original jewelry piece delicately resting on soft, natural beige linen fabric with elegant, flowing folds. Soft, organic directional window lighting casting natural, subtle shadows. High-end lifestyle editorial aesthetic, warm and tactile.",
        "is_model": False
    },
    {
        "key": "social_33_dark_grey_stone",
        "label": "Creative — Dark Grey Stone",
        "shot": "The exact original jewelry piece placed on a raw, textured dark grey stone surface. Moody, directional studio lighting emphasizing the raw, organic texture of the stone against the refined polish of the jewelry. High-end lifestyle editorial aesthetic, earthy and dramatic.",
        "is_model": False
    },
    {
        "key": "social_34_noir_chiaroscuro",
        "label": "Studio — Noir Chiaroscuro",
        "shot": "Ultra-luxury black-and-white studio photography. The exact original jewelry piece illuminated by a sharp, precise optical snoot spotlight against deep, dramatic pitch-black shadows. Extreme high contrast chiaroscuro lighting, emphasizing the geometric brilliance and sharp reflections of the piece. CRITICAL MANDATE: THE JEWELRY ITSELF MUST NOT BE BLACK AND WHITE. The jewelry MUST be in full, highly saturated, true original color.",
        "is_model": False
    },
    {
        "key": "luxury_09_candid_editorial",
        "label": "Luxury Model — Candid Editorial",
        "shot": "High-end luxury editorial model photoshoot. A sophisticated model wearing the exact original jewelry piece, captured in a candid, authentic moment (e.g., adjusting an earring, resting a hand). Soft, diffused natural lighting. The composition uses close-up proximity to focus on the intricate details of the jewelry while blurring the elegant background into a cinematic bokeh, conveying quiet luxury and emotional storytelling.",
        "is_model": True
    },
    {
        "key": "luxury_10_white_shirt_off_shoulder",
        "label": "Luxury Model — White Shirt Casual",
        "shot": "A candid, intimate luxury lifestyle photograph of a young woman wearing the exact reference jewelry. She is wearing a slightly oversized, crisp white button-up shirt that is playfully slipping off one shoulder, beautifully framing her skin. Warm, soft natural window lighting. The aesthetic is cozy, authentic, and high-end editorial. The jewelry is the focal point, perfectly scaled.",
        "is_model": True
    }
]

# We must also import CATEGORIES from the existing generator.py, but since generator.py has it,
# we will dynamically import it or leave it in generator.py for now to avoid circular imports.
# For full scalability, we'll redefine the categories here.
ALIASES = {
    "rings": "ring",
    "band": "ring",
    "wedding band": "ring",
    "engagement ring": "ring",
    "bracelets": "bracelet",
    "bangle": "bracelet",
    "cuff": "bracelet",
    "necklaces": "necklace",
    "pendant": "necklace",
    "chain": "necklace",
    "earrings": "earring",
    "studs": "earring",
    "hoops": "earring",
    "drops": "earring",
    "dangles": "earring"
}

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
            {
                "key":   "10_product_side_profile",
                "label": "Product — 90° Side Band",
                "shot":  (
                    "The ring standing upright on a creamy marble surface, shot from a pure 90-degree side profile. "
                    "Reveals the full band thickness, gallery wire, and stone setting height. "
                    "Crisp natural side lighting, sharp focus on the metal edge and profile."
                ),
            },
            {
                "key":   "11_product_macro_stone",
                "label": "Product — Macro Center Stone",
                "shot":  (
                    "Extreme macro close-up of the ring's center stone on a creamy marble surface. "
                    "Every facet, inclusion, and brilliance pattern razor-sharp. "
                    "Dramatic spotlight-style natural light creating prismatic fire and scintillation. "
                    "Extremely shallow depth of field, background completely dissolved."
                ),
            },
            {
                "key":   "12_product_low_angle_hero",
                "label": "Product — Low Angle Hero",
                "shot":  (
                    "The ring standing upright on a textured natural stone surface, shot from a dramatic low angle "
                    "looking upward. The ring appears monumental and imposing. "
                    "Warm directional lighting from behind, creating a subtle backlit glow around the metal edges. "
                    "Cinematic, editorial hero shot."
                ),
            },
            {
                "key":   "14_product_back_band",
                "label": "Product — Band Back Detail",
                "shot":  (
                    "The back of the ring displayed on a creamy marble surface, showing the inner band, "
                    "hallmarks, and any engraving. Shot straight-on at eye level. "
                    "Clean natural lighting, every stamp and finish detail visible."
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
            {
                "key":   "05_product_chain_macro",
                "label": "Product — Chain Link Macro",
                "shot":  (
                    "Extreme macro close-up of the necklace chain links on a creamy marble surface. "
                    "Shows the craftsmanship, link pattern, and metal finish in microscopic detail. "
                    "Natural directional light catching each polished surface. Extremely shallow depth of field."
                ),
            },
            {
                "key":   "06_product_clasp_detail",
                "label": "Product — Clasp Detail",
                "shot":  (
                    "Close-up of the necklace clasp mechanism on a natural stone surface. "
                    "Shows the lobster claw or spring ring in sharp focus. "
                    "Clean natural lighting, professional product documentation style."
                ),
            },
            {
                "key":   "07_product_draped_curve",
                "label": "Product — Draped S-Curve",
                "shot":  (
                    "The necklace arranged in an elegant S-curve on a luxury creamy marble surface, shot from above at a slight angle. "
                    "The chain flows naturally with organic movement. Pendant rests at the curve's center. "
                    "Soft directional window light, creating depth along the chain's contour."
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
            {
                "key": "13_model_off_shoulder_white_shirt",
                "label": "Model — White Shirt Casual",
                "shot": (
                    "A candid, intimate luxury lifestyle photograph of a young woman wearing the exact reference necklace. "
                    "She is wearing a slightly oversized, crisp white button-up shirt that is playfully slipping off one shoulder, "
                    "beautifully framing her collarbone and neck. Warm, soft natural window lighting. "
                    "The aesthetic is cozy, authentic, and high-end editorial."
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
            {
                "key":   "05_product_side_profile",
                "label": "Product — Side Profile",
                "shot":  (
                    "The bracelet standing upright on a creamy marble surface, shot from a 90-degree side profile. "
                    "Shows the full width, stone settings, and metalwork depth. "
                    "Natural directional lighting, realistic shadow cast."
                ),
            },
            {
                "key":   "06_product_link_macro",
                "label": "Product — Link Macro Detail",
                "shot":  (
                    "Extreme macro close-up of the bracelet links or stone settings on a natural stone surface. "
                    "Every detail of the metalwork and gem mounting visible at microscopic level. "
                    "Shallow depth of field, dramatic natural side lighting."
                ),
            },
            {
                "key":   "07_product_curved_arc",
                "label": "Product — Curved Arc View",
                "shot":  (
                    "The bracelet displayed in a natural curved arc on a creamy marble surface, shot from a slight overhead angle. "
                    "Shows the natural curvature and how stones flow along the band. "
                    "Soft natural window light, elegant and organic presentation."
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
            {
                "key":   "05_product_back_post",
                "label": "Product — Back & Post Detail",
                "shot":  (
                    "One earring flipped to show the back, post, and butterfly clutch on a creamy marble surface. "
                    "All mechanical details clearly visible. Clean, even natural lighting. "
                    "Professional product documentation, sharp focus on the findings."
                ),
            },
            {
                "key":   "06_product_macro_stone",
                "label": "Product — Macro Stone Detail",
                "shot":  (
                    "Extreme macro close-up of one earring's center stone or diamond cluster on a natural stone surface. "
                    "Every facet and brilliance pattern captured in microscopic detail. "
                    "Dramatic natural spotlight creating prismatic fire. Extremely shallow depth of field."
                ),
            },
            {
                "key":   "07_product_staggered_pair",
                "label": "Product — Staggered Pair Display",
                "shot":  (
                    "Both earrings displayed at staggered heights on creamy marble surfaces or small stone pedestals. "
                    "One slightly forward, one slightly behind, creating elegant depth and dimension. "
                    "Soft directional natural lighting, luxury editorial display style."
                ),
            },
            {
                "key":   "08_product_drop_length",
                "label": "Product — Drop Length Profile",
                "shot":  (
                    "One earring hanging vertically against a creamy marble background, showing full drop length. "
                    "Shot straight-on to reveal total dimensions and dangle movement. "
                    "Natural side lighting, clean proportional reference."
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
            {
                "key": "13_model_off_shoulder_white_shirt",
                "label": "Model — White Shirt Casual",
                "shot": (
                    "A candid, intimate luxury lifestyle photograph of a young woman wearing the exact reference earring. "
                    "CRITICAL SIZE REQUIREMENT: The earring must be rendered VERY SMALL and delicate on her earlobe. "
                    "She is wearing a slightly oversized, crisp white button-up shirt that is playfully slipping off one shoulder, "
                    "beautifully framing her neck and ear. Warm, soft natural window lighting. "
                    "The aesthetic is cozy, authentic, and high-end editorial."
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
            {
                "key":   "05_product_bail_macro",
                "label": "Product — Bail Close-Up",
                "shot":  (
                    "Extreme macro close-up of the pendant bail and chain attachment on a creamy marble surface. "
                    "Shows the loop, metalwork, and how the chain threads through. "
                    "Natural directional light, sharp focus on the craftsmanship details."
                ),
            },
            {
                "key":   "06_product_side_profile",
                "label": "Product — Side Depth Profile",
                "shot":  (
                    "The pendant on a natural stone surface, shot from a 90-degree side profile. "
                    "Reveals the full depth, stone setting height, and bezel or prong work. "
                    "Clean natural side lighting, professional documentation angle."
                ),
            },
            {
                "key":   "07_product_macro_stone",
                "label": "Product — Stone Facet Macro",
                "shot":  (
                    "Extreme macro close-up of the pendant's center stone on a creamy marble surface. "
                    "Every facet, fire, and brilliance pattern captured with razor-sharp precision. "
                    "Dramatic spotlight-style natural light. Extremely shallow depth of field."
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
            {
                "key": "10_model_off_shoulder_white_shirt",
                "label": "Model — White Shirt Casual",
                "shot": (
                    "A candid, intimate luxury lifestyle photograph of a young woman wearing the exact reference pendant. "
                    "She is wearing a slightly oversized, crisp white button-up shirt that is playfully slipping off one shoulder, "
                    "beautifully framing her collarbone and neck. Warm, soft natural window lighting. "
                    "The aesthetic is cozy, authentic, and high-end editorial."
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
            {
                "key":   "05_product_interior",
                "label": "Product — Interior Detail",
                "shot":  (
                    "The bangle tilted to reveal the interior surface on a creamy marble surface. "
                    "Shows any engravings, hallmarks, or smooth interior finish. "
                    "Clean natural lighting from above, sharp focus on interior details."
                ),
            },
            {
                "key":   "06_product_low_angle",
                "label": "Product — Low Angle Hero",
                "shot":  (
                    "The bangle standing upright on a textured natural stone surface, shot from a dramatic low angle. "
                    "The bangle appears monumental and imposing against a soft-focus background. "
                    "Warm directional backlight creating a subtle glow around the metal edges."
                ),
            },
            {
                "key":   "07_product_stacked",
                "label": "Product — Stacked Display",
                "shot":  (
                    "The bangle displayed alongside two complementary thin metal bands on a creamy marble surface. "
                    "Stacked arrangement showing versatility and styling potential. "
                    "Soft natural window light, luxury editorial display style."
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
            {
                "key":   "05_product_clasp_detail",
                "label": "Product — Clasp Detail",
                "shot":  (
                    "Close-up of the anklet clasp mechanism on a natural stone surface. "
                    "Shows the closure type and extension chain clearly. "
                    "Sharp focus, clean natural lighting, professional documentation."
                ),
            },
            {
                "key":   "06_product_coiled_circle",
                "label": "Product — Coiled Circle",
                "shot":  (
                    "The anklet coiled in a natural circle on a creamy marble surface, shot from above. "
                    "Shows the complete chain pattern and charms in a compact, elegant arrangement. "
                    "Soft natural overhead light, organic presentation."
                ),
            },
            {
                "key":   "07_product_chain_macro",
                "label": "Product — Chain Link Macro",
                "shot":  (
                    "Extreme macro close-up of the anklet chain links on a natural stone surface. "
                    "Shows the link pattern, metal finish, and craftsmanship in microscopic detail. "
                    "Natural directional light, extremely shallow depth of field."
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
            {
                "key":   "05_product_back_pin",
                "label": "Product — Back Pin Mechanism",
                "shot":  (
                    "The brooch flipped to show the back, revealing the pin mechanism, catch, and hinge. "
                    "Laid flat on a creamy marble surface. Clean natural lighting. "
                    "Professional documentation shot showing construction quality."
                ),
            },
            {
                "key":   "06_product_low_angle",
                "label": "Product — Low Angle Perspective",
                "shot":  (
                    "The brooch propped at a slight angle on a natural stone surface, shot from a dramatic low angle. "
                    "Creates a monumental, heroic perspective emphasizing the brooch's sculptural quality. "
                    "Warm backlit glow, cinematic depth of field."
                ),
            },
            {
                "key":   "07_product_texture_macro",
                "label": "Product — Texture & Enamel Macro",
                "shot":  (
                    "Extreme macro close-up of the brooch surface on a creamy marble surface. "
                    "Captures enamel work, filigree, milgrain, or engraved details at microscopic level. "
                    "Natural directional light revealing surface textures. Ultra-shallow depth of field."
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
