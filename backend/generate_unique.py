import argparse
import asyncio
from pathlib import Path
from google import genai
from google.genai import types

# Use the same API key as your backend
GEMINI_API_KEY = "AIzaSyBRYRW4UxifNDI65wArxv0wWbDcACXWuyI"
MODEL = "gemini-2.5-flash-image"

async def generate_unique_design(image_path: str):
    path = Path(image_path)
    if not path.exists():
        print(f"Error: Image '{image_path}' not found.")
        return

    print(f"Reading image: {path.name}...")
    img_bytes = path.read_bytes()
    mime_type = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"

    # Initialize Gemini client
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Custom prompt completely deviating from the strict "copy" rules
    # and instead instructing the model to get creative.
    prompt = """
You are a highly creative luxury jewelry designer. 
Analyze the provided reference image for its general vibe, but DO NOT copy the design exactly. 
Your task is to generate a completely NEW, DIFFERENT, and UNIQUE jewelry design inspired by it.

CREATIVE INSTRUCTIONS:
- Change the overall structure or shape to make it unique.
- Incorporate different types of precious stones, different cuts (e.g., from round to emerald cut or pear shape), and new color palettes.
- Alter the metal work (e.g., change from plain polished gold to hammered texture, or mix metals).
- Add intricate details or modern minimalist touches that differ from the original.

PHOTOGRAPHY STYLE:
- Render this as a high-end luxury product shot.
- Soft, directional natural side-window lighting that creates elegant shadows.
- Beautiful, textured cinematic background (like dark silk, natural stone, or marble).
- Photorealistic quality with sharp focus on the new jewelry piece.
"""

    print("Generating a new, unique design. Please wait...")
    try:
        resp = await client.aio.models.generate_content(
            model=MODEL,
            contents=[
                types.Part.from_bytes(data=img_bytes, mime_type=mime_type),
                types.Part.from_text(text=prompt)
            ],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
            ),
        )

        # Save the returned image
        for part in resp.candidates[0].content.parts:
            inline_data = getattr(part, "inline_data", None)
            if inline_data:
                out_bytes = inline_data.data
                ext = "png" if "png" in getattr(inline_data, "mime_type", "") else "jpg"
                
                # Save next to the original file
                out_filename = f"unique_reimagined_{path.stem}.{ext}"
                out_path = Path.cwd() / out_filename
                out_path.write_bytes(out_bytes)
                
                print(f"Success! ✨ Unique design generated and saved to: {out_path.absolute()}")
                return

        print("Failed to generate an image from the response.")
    except Exception as e:
        print(f"An error occurred during generation: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a completely new and unique jewelry design inspired by a reference image.")
    parser.add_argument("image_path", help="Path to the reference image you want to upload.")
    args = parser.parse_args()
    
    # Run the async generation function
    asyncio.run(generate_unique_design(args.image_path))
