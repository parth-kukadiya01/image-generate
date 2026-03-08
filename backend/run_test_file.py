import asyncio
from generator import generate_shots

async def main():
    try:
        dummy_jpg = bytes.fromhex("FFD8FFE000104A46494600010101004800480000FFDB004300080606070605080707070909080A0C140D0C0B0B0C1912130F141D1A1F1E1D1A1C1C20242E2720222C231C1C2837292C30313434341F27393D38323C2E333432FFD9")
        results = await generate_shots(dummy_jpg, "image/jpeg", "ring", "test_session_file")
        print(f"Success! Generated {len(results)} images")
        for r in results:
            print(f" - {r['label']}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
