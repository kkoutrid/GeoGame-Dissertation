"""Local script: exports the desktop game's Desktop/GameAssets/geodata.xlsx to GameAssets/geodata.json
for the web build (which drops pandas/openpyxl at runtime). Run with a Python
environment that has pandas+openpyxl installed; not shipped/executed in the browser.
"""
import json
import os

import pandas as pd

root_dir = os.path.dirname(os.path.abspath(__file__))
# Single source of truth: the same Excel the desktop game reads, so costs and
# level data are edited in one place. Re-run this, then rebuild, after editing it.
xlsx_path = os.path.join(root_dir, "..", "Desktop", "GameAssets", "geodata.xlsx")
json_path = os.path.join(root_dir, "GameAssets", "geodata.json")

na_icons = pd.read_excel(xlsx_path, sheet_name="na_icons").to_dict(orient="list")
pipe_connections = pd.read_excel(xlsx_path, sheet_name="pipe_connections").to_dict(orient="list")
info = pd.read_excel(xlsx_path, sheet_name="info").to_dict(orient="list")

data = {
    "na_icons": na_icons,
    "pipe_connections": pipe_connections,
    "info": info,
}

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(data, f)

print(f"Wrote {json_path}")
