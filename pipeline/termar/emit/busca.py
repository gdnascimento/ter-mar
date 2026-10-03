"""Write ``site/data/busca.json``, the autocomplete index."""

from __future__ import annotations

from pathlib import Path


def normalize(name: str) -> str:
    """Lowercase and strip accents, for accent-insensitive matching.

    Precomputed here so the browser never normalises 5,570 strings at load.
    """
    raise NotImplementedError


def write(out_dir: Path) -> Path:
    """Emit the ``[code, name, uf, normalized]`` rows."""
    raise NotImplementedError
