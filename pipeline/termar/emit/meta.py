"""Write ``site/data/meta.json``.

Every other emitted file is uninterpretable without this one: it carries the
window, the extraction date, the thresholds, the model diagnostics and the
per-view priors and overdispersion factors.
"""

from __future__ import annotations

from pathlib import Path


def write(out_dir: Path) -> Path:
    """Emit ``meta.json`` per ``schemas/meta.schema.json``.

    ``expected_false_flags`` is ``municipalities_published * verdict_alpha`` and
    is stated in words on the methodology page, so a reader knows roughly how
    many flags are chance.
    """
    raise NotImplementedError
