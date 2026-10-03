"""Central settings: every window, threshold, vintage and version string.

No other module defines a threshold. If a number governs behaviour, it lives
here and is echoed into ``meta.json`` so a published figure can always be traced
back to the settings that produced it.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

View = str
"""Either ``"residence"`` or ``"provider"``. The two are never merged (invariant 5)."""

VIEWS: tuple[View, View] = ("residence", "provider")


@dataclass(frozen=True, slots=True)
class Window:
    """A closed month range, inclusive at both ends."""

    start: str
    """``YYYY-MM``."""

    end: str
    """``YYYY-MM``."""

    @property
    def label(self) -> str:
        """Human label for the page header, e.g. ``2021-2023``."""
        raise NotImplementedError

    def months(self) -> list[tuple[int, int]]:
        """Every ``(year, month)`` in the window, ascending."""
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Suppression:
    """Thresholds below which no estimate is published (invariant 3).

    Simultaneously a statistical necessity and a small-cell disclosure
    safeguard. Do not relax either value to increase map coverage.
    """

    min_expected_deaths: float = 5.0
    min_stays: int = 30


@dataclass(frozen=True, slots=True)
class Settings:
    """Everything that governs a pipeline run."""

    window: Window
    suppression: Suppression
    verdict_alpha: float
    """0.002, the 99.8% limit. Not 0.05 -- see docs/02-methodology.md section 8."""

    ibge_vintage: str
    """Four-digit year of the IBGE municipality vintage. Boundaries move."""

    model_version: str
    """Stamped into every emitted file. Change it whenever the model changes."""

    datasus_extracted_at: date | None = None
    """Set by the ingest step. DATASUS revises history; without this two runs
    are not comparable."""

    reference_model_kind: str = "stratified"
    """``"stratified"`` (M3) or ``"logistic"`` (M5)."""

    overdispersion_winsorise: tuple[float, float] = (0.10, 0.90)
    """Quantiles at which variance-stabilised residuals are winsorised before
    estimating phi, so genuine outliers do not inflate it."""


SETTINGS = Settings(
    window=Window(start="2021-01", end="2023-12"),
    suppression=Suppression(),
    verdict_alpha=0.002,
    ibge_vintage="2022",
    model_version="2026-10-02-stratified-v1",
)
