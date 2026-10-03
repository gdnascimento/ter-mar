"""Shared fixtures and the stub-skip mechanism.

At milestone M0 every function in ``pipeline/termar`` raises
``NotImplementedError``. The tests below are written in full anyway: they are
the specification, and they run for real the moment a stub is implemented.

The hook below turns ``NotImplementedError`` raised by a stub into a skip, so
the suite is green on a fresh clone while the number of unimplemented pieces
stays loudly visible in the summary.

THIS IS NOT AN ESCAPE HATCH. Raising ``NotImplementedError`` from code that is
supposed to work, in order to make a failing test skip, is forbidden by
``AGENTS.md``. The count printed at the end of every run should only ever go
down.
"""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"

_stub_skips: list[str] = []


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item: pytest.Item):  # noqa: ANN201
    """Convert NotImplementedError from an unimplemented stub into a skip."""
    outcome = yield
    try:
        outcome.get_result()
    except NotImplementedError:
        _stub_skips.append(item.nodeid)
        pytest.skip("stub not implemented yet")


def pytest_terminal_summary(terminalreporter, exitstatus, config) -> None:  # noqa: ANN001, ARG001
    """Print how many tests are waiting on a stub."""
    if _stub_skips:
        terminalreporter.write_sep("-", f"{len(_stub_skips)} test(s) waiting on stubs")
        for nodeid in _stub_skips:
            terminalreporter.write_line(f"  {nodeid}")


def _read_csv(name: str) -> list[dict[str, str]]:
    with (FIXTURES / name).open(newline="", encoding="utf-8") as fh:
        return [row for row in csv.DictReader(fh) if not row["N_AIH"].startswith("#")]


@pytest.fixture(scope="session")
def aih_chains() -> list[dict[str, str]]:
    """Hand-built AIH records covering every collapse case in docs/06-acceptance.md."""
    return _read_csv("aih_chains.csv")


@pytest.fixture(scope="session")
def expected_stays() -> list[dict[str, str]]:
    """The collapse of aih_chains, computed by hand. The oracle for test_stays."""
    return _read_csv("expected_stays.csv")
