"""One-off local script: exports geodata_source.xlsx to GameAssets/geodata.json
for the web build (which drops pandas/openpyxl at runtime). Run with a Python
environment that has pandas+openpyxl installed; not shipped/executed in the browser.
"""
import json
import os

import pandas as pd

root_dir = os.path.dirname(os.path.abspath(__file__))
xlsx_path = os.path.join(root_dir, "geodata_source.xlsx")
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
