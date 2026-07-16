"""Browser localStorage-backed persistence for per-level high scores, replacing
the desktop version's read/write into geodata.xlsx (which has no equivalent in
a browser sandbox). Falls back to an in-memory dict when not running under
pygbag/emscripten (e.g. a quick local syntax check with plain CPython).
"""
import json

_STORAGE_KEY = "geogame_high_scores_v1"
_memory_store = {}


def _get_local_storage():
    # `js` only exists inside a pyodide/emscripten (browser) runtime; trying the
    # import is more reliable than matching a platform-string spelling.
    try:
        import js
        return js.window.localStorage
    except Exception:
        return None


def _load():
    storage = _get_local_storage()
    if storage is None:
        return dict(_memory_store)
    raw = storage.getItem(_STORAGE_KEY)
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except (ValueError, TypeError):
        return {}


def _save(data):
    storage = _get_local_storage()
    if storage is None:
        _memory_store.clear()
        _memory_store.update(data)
        return
    storage.setItem(_STORAGE_KEY, json.dumps(data))


def seed_defaults(dataset_indices, base_high_scores):
    """Populate storage with the shipped default high scores for any dataset
    not already present, so a first-time player sees the same baseline the
    desktop version ships with."""
    data = _load()
    changed = False
    for i, dataset in enumerate(dataset_indices):
        key = str(dataset)
        if key not in data:
            data[key] = base_high_scores[i] if base_high_scores[i] is not None else 0
            changed = True
    if changed:
        _save(data)


def get_high_score(dataset):
    data = _load()
    return data.get(str(dataset), 0)


def get_all_high_scores(dataset_indices):
    data = _load()
    return [data.get(str(d), 0) for d in dataset_indices]


def set_high_score(dataset, score):
    """Updates the stored high score only if `score` beats the current one,
    mirroring update_high_score()'s original behaviour. Returns the resulting
    (possibly unchanged) high score."""
    data = _load()
    key = str(dataset)
    current = data.get(key, 0) or 0
    if score > current:
        data[key] = score
        _save(data)
        return score
    return current


def reset_high_scores(dataset_indices):
    data = _load()
    for dataset in dataset_indices:
        data[str(dataset)] = 0
    _save(data)
