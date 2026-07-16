"""Trigger a browser file download from in-memory bytes, replacing the desktop
version's direct writes to disk (pygame.image.save to GameAssets/Results).
No-ops outside a pyodide/emscripten browser runtime.
"""
import base64


def trigger_download(data_bytes, filename, mime="application/octet-stream"):
    try:
        import js
    except Exception:
        print(f"[web] Download unavailable outside the browser; skipped {filename}")
        return
    b64 = base64.b64encode(data_bytes).decode("ascii")
    data_url = f"data:{mime};base64,{b64}"
    anchor = js.document.createElement("a")
    anchor.href = data_url
    anchor.download = filename
    js.document.body.appendChild(anchor)
    anchor.click()
    js.document.body.removeChild(anchor)
