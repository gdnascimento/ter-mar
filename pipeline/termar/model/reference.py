"""The national case-mix reference model.

Always fitted on the **national** pool, never per state: the full stratum cross
product is 2,400 cells, which is tractable nationally and is not per UF.

Pure with respect to the filesystem: these classes take and return frames and
arrays. That is what makes them testable.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import numpy as np
import polars as pl
from numpy.typing import NDArray


@dataclass(frozen=True, slots=True)
class ModelDiagnostics:
    """Published on the methodology page and carried in ``meta.json``."""

    kind: str
    c_statistic: float
    """Expect 0.75-0.80. Above 0.85 on this data indicates outcome leakage --
    most likely a covariate that encodes death."""

    strata_count: int
    collapsed_strata: int
    calibration: pl.DataFrame
    """Observed vs predicted by decile of predicted risk. The top decile matters
    most: that is where regional hubs sit."""


class ReferenceModel(Protocol):
    """Interface shared by the stratified and logistic implementations."""

    def fit(self, stays: pl.DataFrame) -> None:
        """Fit on the national stay-level table with case-mix columns."""
        ...

    def predict(self, stays: pl.DataFrame) -> NDArray[np.float64]:
        """Predicted death probability per stay."""
        ...

    def diagnostics(self) -> ModelDiagnostics:
        """Fit quality, for publication."""
        ...


class StratifiedReference:
    """Milestone M3. Expected probability is the national rate in the stratum.

    Strata with fewer than 30 national stays collapse upward by dropping
    ``icu_days_band`` first, then ``admission_type``. Transparent, no fitting,
    easy to audit.
    """

    def fit(self, stays: pl.DataFrame) -> None:  # noqa: D102
        raise NotImplementedError

    def predict(self, stays: pl.DataFrame) -> NDArray[np.float64]:  # noqa: D102
        raise NotImplementedError

    def diagnostics(self) -> ModelDiagnostics:  # noqa: D102
        raise NotImplementedError


class LogisticReference:
    """Milestone M5. Logistic regression with splines on age and ICU days."""

    def fit(self, stays: pl.DataFrame) -> None:  # noqa: D102
        raise NotImplementedError

    def predict(self, stays: pl.DataFrame) -> NDArray[np.float64]:  # noqa: D102
        raise NotImplementedError

    def diagnostics(self) -> ModelDiagnostics:  # noqa: D102
        raise NotImplementedError


def c_statistic(outcome: NDArray[np.int64], predicted: NDArray[np.float64]) -> float:
    """Area under the ROC curve."""
    raise NotImplementedError


def calibration_by_decile(
    outcome: NDArray[np.int64], predicted: NDArray[np.float64]
) -> pl.DataFrame:
    """Observed and predicted death rates by decile of predicted risk."""
    raise NotImplementedError
