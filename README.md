# GeoGame

A geothermal heating network puzzle game — MSc dissertation project by
Yiannis Kontos & Konstantinos Koutridis.

## Play it

- **In your browser (no install):** https://kkoutrid.github.io/geogame-web/
- Also on itch.io: https://kkoutrid.itch.io/geogame (recommended)
- **Windows desktop:** download the installer from the
  [Releases](https://github.com/kkoutrid/GeoGame-Dissertation/releases) page.

## About

Place pipes to build a geothermal district-heating network, balancing flow and
temperature to supply houses and greenhouses. The browser version is a
[pygbag](https://github.com/pygame-web/pygbag) (WebAssembly) port of the desktop
pygame game.

## Repository layout

**The two current versions**

- **`Desktop/`** – the Windows/Linux game you install or run with Python.
  - `Geogame92.py` – the game itself.
  - `GameAssets/` – pictures, sounds, fonts and `geodata.xlsx` (levels, pipe
    costs, budgets).
  - `Geogame92.spec`, `Geogame92.iss`, `Geogame.ico` – recipes for turning the
    game into `Geogame92_Setup.exe`.
- **`Web/`** – the browser game (the same game, adapted to run in a web page).
  - `main.py` – the game itself.
  - `build/web/` – the finished website; this is what is uploaded to GitHub
    Pages and itch.io.

**Everything else**

- **`Old versions/Desktop/`** – earlier desktop games (Geogame80 to Geogame91),
  kept for reference. Not needed to play or build the current version.
- **`Old versions/Web/`** – earlier browser builds (GeogameWeb to GeogameWeb6).
- **`Tools/`** – side projects: the server that emails bug reports, and
  bot-training experiments.

## How to run and build it yourself

You only need this section if you want to change the game. Players should use
the links at the top.

Commands are typed in a terminal opened in this folder, with Python 3 installed.

1. **Play the desktop game from the source code**

   ```
   cd Desktop
   pip install -r requirements.txt
   python Geogame92.py
   ```

   The first line enters the game folder, the second installs the libraries the
   game needs (pygame, numpy, pandas, …), the third starts the game.

2. **Change levels or costs.** Edit `Desktop/GameAssets/geodata.xlsx`. The
   browser game reads a copy of this file, so update the copy with:

   ```
   python Web/geodata_export.py
   ```

3. **Rebuild the browser game**

   ```
   pip install pygbag
   python -m pygbag --build --title GeoGame Web
   ```

   This writes a new website to `Web/build/web/`. Upload that folder to update
   the online game.

4. **Make a new Windows installer.** This PC does not have to be Windows:
   GitHub builds it automatically. Push a tag whose name starts with `v`
   (for example `v1.2`); a few minutes later `Geogame92_Setup.exe` appears on
   the Releases page. To test without publishing, open the **Actions** tab and
   run **Build Windows installer** by hand. The steps are in
   `.github/workflows/build-windows.yml`.
