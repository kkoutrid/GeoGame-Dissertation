# GeoGame

A geothermal heating network puzzle game — MSc dissertation project by
Yiannis Kontos & Konstantinos Koutridis.

## Play it

- **In your browser (no install):** https://kkoutrid.github.io/geogame-web/
- Also on itch.io: https://kkoutrid.itch.io/geogame (recommended)
- **Windows desktop:** download the installer from the
  [Releases](../../releases) page.

## About

Place pipes to build a geothermal district-heating network, balancing flow and
temperature to supply houses and greenhouses. The browser version is a
[pygbag](https://github.com/pygame-web/pygbag) (WebAssembly) port of the desktop
pygame game.

## Repository layout

| Folder | Contents |
|---|---|
| `Desktop/` | **Current desktop game** (`Geogame92.py`) with its `GameAssets/`, plus `Geogame92.spec` (PyInstaller) and `Geogame92.iss` (Inno Setup) for the Windows installer. |
| `Web/` | **Current browser game** (pygbag port). `build/web/` is the deployable site. |
| `Old versions/Desktop/` | Earlier desktop versions (Geogame80–91, the 2024 `Currentmodels` set, older files and 2023 snapshots). |
| `Old versions/Web/` | Earlier browser builds (GeogameWeb–GeogameWeb6, WASM backup). |
| `Tools/` | Email backend for bug reports, bot-training experiments and helper scripts. |

Level data and costs (pipe costs, aux cost per degree, budgets) live in
`Desktop/GameAssets/geodata.xlsx`. The browser version uses the same file:
after editing it, run `python Web/geodata_export.py` and rebuild the web game.

## Running and building

- **Desktop from source:** `cd Desktop && pip install -r requirements.txt && python Geogame92.py`
- **Browser build:** `pip install pygbag && python -m pygbag --build --title GeoGame Web`
- **Windows installer:** built by GitHub Actions (`.github/workflows/build-windows.yml`)
  on every `v*` tag and published on the Releases page; it can also be run
  manually from the Actions tab.
