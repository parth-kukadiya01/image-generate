import asyncio
from generator import generate_shots
import aiohttp
import mimetypes

async def download_image(url: str) -> tuple[bytes, str]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise ValueError(f"Failed to download image from {url}")
            
            content_type = response.headers.get('Content-Type', '')
            if not content_type.startswith('image/'):
                content_type = mimetypes.guess_type(url)[0] or 'image/jpeg'
                
            contents = await response.read()
            return contents, content_type

async def main():
    try:
        url = "https://i.etsystatic.com/26792671/r/il/697921/3081519787/il_1588xN.3081519787_1b0q.jpg"
        img, mime = await download_image(url)
        results = await generate_shots(img, mime, "ring", "test_session_angles")
        print(f"Success! Generated {len(results)} images")
        for r in results:
            print(f" - {r['label']}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
