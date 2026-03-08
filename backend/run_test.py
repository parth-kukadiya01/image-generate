import asyncio
from generator import generate_shots_from_text

async def main():
    try:
        results = await generate_shots_from_text("diamond ring", "ring", "test_session_angles")
        print(f"Success! Generated {len(results)} images")
        for r in results:
            print(f" - {r['label']}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
