"""Browser localStorage-backed persistence for per-level high scores, replacing
the desktop version's read/write into geodata.xlsx (which has no equivalent in
a browser sandbox). Falls back to an in-memory dict when not running under
pygbag/emscripten (e.g. a quick local syntax check with plain CPython).
"""
import json

_STORAGE_KEY = "geogame_high_scores_v1"
_memory_store = {}

# Whether per-player progress (high scores / the green "completed" level
# markers) survives across browser sessions. For the permanent public web
# build we want every new visit to start from a clean slate -- all levels
# uncompleted -- so this is False: progress is kept only in memory for the
# current page session and is gone as soon as the page is reloaded or
# reopened (pygbag re-runs the program from scratch on every load, which
# re-initialises _memory_store). Flip to True to restore the old behaviour of
# persisting each browser's progress in localStorage.
PERSIST_PROGRESS = False


def _get_local_storage():
    # When progress is session-only we never touch localStorage, so treat it as
    # unavailable and fall back to the in-memory store. Any stale data a browser
    # saved under the old persistent behaviour is simply ignored, not read.
    if not PERSIST_PROGRESS:
        return None
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
    """Start every session with all levels uncompleted.

    The shipped desktop data marks Level 1 as already solved (high score
    4010), and the level-select screen draws a green "completed" border around
    any level whose high score is > 0. For the permanent public web build we
    ignore those baked-in scores and seed 0 for every level, so a fresh session
    shows no completed levels. `base_high_scores` is kept in the signature for
    call-site compatibility but intentionally unused. (With PERSIST_PROGRESS
    False nothing is written to localStorage anyway -- this just fills the
    in-memory store for the current session.)"""
    data = _load()
    changed = False
    for dataset in dataset_indices:
        key = str(dataset)
        if key not in data:
            data[key] = 0
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
