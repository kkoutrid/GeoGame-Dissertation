"""One-off local script: exports geodata_source.xlsx to GameAssets/geodata.json
(read by Python at runtime) and static/geodata.json (a plain-served copy fetched
directly by the HTML/JS menu shell -- pygbag only exposes a project's `static/`
folder as loose files; everything else is packed into the .apk). Run with a Python
environment that has pandas+openpyxl installed; not shipped/executed in the browser.
"""
import json
import math
import os

import pandas as pd

root_dir = os.path.dirname(os.path.abspath(__file__))
xlsx_path = os.path.join(root_dir, "geodata_source.xlsx")
json_path = os.path.join(root_dir, "GameAssets", "geodata.json")
static_json_path = os.path.join(root_dir, "static", "geodata.json")

na_icons = pd.read_excel(xlsx_path, sheet_name="na_icons").to_dict(orient="list")
pipe_connections = pd.read_excel(xlsx_path, sheet_name="pipe_connections").to_dict(orient="list")
info = pd.read_excel(xlsx_path, sheet_name="info").to_dict(orient="list")

data = {
    "na_icons": na_icons,
    "pipe_connections": pipe_connections,
    "info": info,
}


def _sanitize_nan(obj):
    """Replaces float('nan') with None so the output is standard JSON (JS's
    JSON.parse rejects the literal NaN token that Python's json module emits
    by default, even though Python's own json.load tolerates it)."""
    if isinstance(obj, float) and math.isnan(obj):
        return None
    if isinstance(obj, list):
        return [_sanitize_nan(v) for v in obj]
    if isinstance(obj, dict):
        return {k: _sanitize_nan(v) for k, v in obj.items()}
    return obj


data = _sanitize_nan(data)

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(data, f)
os.makedirs(os.path.dirname(static_json_path), exist_ok=True)
with open(static_json_path, "w", encoding="utf-8") as f:
    json.dump(data, f)

print(f"Wrote {json_path}")
print(f"Wrote {static_json_path}")
