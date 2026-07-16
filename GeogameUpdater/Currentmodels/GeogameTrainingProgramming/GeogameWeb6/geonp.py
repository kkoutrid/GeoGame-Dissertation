"""geonp -- a tiny pure-Python stand-in for the sliver of numpy that
GeogameWeb uses.

Why this exists: pygbag has to download the numpy wheel (~3.8 MB) from the
pygame-web CDN at boot, and those CDN fetches truncate in the browser, so
`import numpy` fails with ModuleNotFoundError and the game never starts. The
game only touches a shallow corner of numpy (array/astype/reshape/concatenate/
append plus scalar-and-1-element-list arithmetic in the thermal sim), so we
replace it with this bundled module -- no runtime download, works on any host.

Semantics mirror numpy for the operations the game actually performs:
elementwise +-*/ with size-1 broadcasting, float() on size-1 arrays, row-major
reshape, and int()/float() casts that truncate toward zero like numpy's astype.
Import as `import geonp as np`.
"""


def _data(obj):
    """Return the backing list for an ndarray / list / tuple, or wrap a scalar
    as a size-1 list (numpy treats np.array(scalar) as a 0-d array that
    broadcasts like a single element)."""
    if isinstance(obj, ndarray):
        return obj._d
    if isinstance(obj, (list, tuple)):
        return list(obj)
    return [obj]


class ndarray:
    __slots__ = ("_d",)

    def __init__(self, data):
        # data is already a plain list (1-D of scalars, or 2-D as list-of-lists
        # after reshape). Callers go through array()/reshape()/etc.
        self._d = data

    # ---- shape/lookup -----------------------------------------------------
    def __len__(self):
        return len(self._d)

    def __getitem__(self, i):
        v = self._d[i]
        # wrap nested rows (2-D) and slices so [x][y] and iteration keep working
        if isinstance(v, list):
            return ndarray(v)
        return v

    def __iter__(self):
        for v in self._d:
            yield ndarray(v) if isinstance(v, list) else v

    def __float__(self):
        if len(self._d) != 1:
            raise TypeError("only size-1 arrays can be converted to Python scalars")
        return float(self._d[0])

    def __repr__(self):
        return "geonp.array(%r)" % (self._d,)

    # ---- casts ------------------------------------------------------------
    def astype(self, dtype):
        if dtype is None:
            return ndarray(list(self._d))
        return ndarray([dtype(v) for v in self._d])

    def tolist(self):
        return [v.tolist() if isinstance(v, ndarray) else v for v in self._d]

    # ---- elementwise arithmetic (numpy-style size-1 broadcasting) ---------
    def _binop(self, other, op, reflected=False):
        a = list(self._d)
        b = _data(other)
        if len(a) == 1 and len(b) != 1:
            a = a * len(b)
        elif len(b) == 1 and len(a) != 1:
            b = b * len(a)
        if len(a) != len(b):
            raise ValueError("operands could not be broadcast together: %d vs %d"
                             % (len(a), len(b)))
        if reflected:
            return ndarray([op(y, x) for x, y in zip(a, b)])
        return ndarray([op(x, y) for x, y in zip(a, b)])

    def __add__(self, o):
        return self._binop(o, lambda x, y: x + y)

    def __radd__(self, o):
        return self._binop(o, lambda x, y: x + y)

    def __sub__(self, o):
        return self._binop(o, lambda x, y: x - y)

    def __rsub__(self, o):
        return self._binop(o, lambda x, y: x - y, reflected=True)

    def __mul__(self, o):
        return self._binop(o, lambda x, y: x * y)

    def __rmul__(self, o):
        return self._binop(o, lambda x, y: x * y)

    def __truediv__(self, o):
        return self._binop(o, lambda x, y: x / y)

    def __rtruediv__(self, o):
        return self._binop(o, lambda x, y: x / y, reflected=True)

    def __neg__(self):
        return ndarray([-x for x in self._d])


# ---- module-level constructors -------------------------------------------
def array(obj, dtype=None):
    a = ndarray(_data(obj) if not isinstance(obj, ndarray) else list(obj._d))
    return a.astype(dtype) if dtype is not None else a


def concatenate(seqs):
    out = []
    for s in seqs:
        out.extend(_data(s))
    return ndarray(out)


def append(a, values):
    return ndarray(_data(a) + _data(values))


def reshape(a, shape):
    flat = _data(a)
    rows, cols = shape
    return ndarray([flat[r * cols:(r + 1) * cols] for r in range(rows)])
