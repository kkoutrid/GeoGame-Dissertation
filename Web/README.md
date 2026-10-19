# Browser version

The current browser version of GeoGame. It is the same game as `Desktop/`,
adapted with [pygbag](https://github.com/pygame-web/pygbag) so it runs in a web page.

Play it at https://kkoutrid.github.io/geogame-web/ or https://kkoutrid.itch.io/geogame.

| File / folder | What it is |
|---|---|
| `main.py` | The game |
| `GameAssets/` | Pictures, sounds, fonts and `geodata.json` (the level data, converted from the desktop Excel file) |
| `geonp.py` | Small replacement for the parts of numpy the game uses, since numpy can't be loaded reliably in the browser |
| `webstorage.py` | Remembers the player's name and high scores in the browser |
| `webdownload.py` | Lets the player download a picture of their solution |
| `geodata_export.py` | Converts `Desktop/GameAssets/geodata.xlsx` into `GameAssets/geodata.json` |
| `build/web/` | The finished website, as uploaded to GitHub Pages and itch.io |
