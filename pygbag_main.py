import asyncio
import sys
import traceback

print("pygbag_main.py: Starting imports", file=sys.stderr)
from main import Game
print("pygbag_main.py: Imports completed", file=sys.stderr)

async def main():
    try:
        print("pygbag_main.py: Starting main function", file=sys.stderr)
        game = Game()
        print("pygbag_main.py: Game instance created", file=sys.stderr)
        await game.run_async()
    except Exception as e:
        print(f"pygbag_main.py: Error in main function: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)

print("pygbag_main.py: About to run main function", file=sys.stderr)
asyncio.run(main())
print("pygbag_main.py: Main function completed", file=sys.stderr)