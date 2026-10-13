import re

with open('Geogame_WASM/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# We want to extract the game_over function to see exactly how to fix it.
match = re.search(r'async def game_over\(\):(.*?)(?=\nasync def|\n\s*def|\n\n\n)', content, re.DOTALL)
if match:
    game_over_code = match.group(0)
    with open('game_over_debug.txt', 'w', encoding='utf-8') as debug_f:
        debug_f.write(game_over_code)
    print("Extracted game_over")
else:
    print("Could not find game_over")
