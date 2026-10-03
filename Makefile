# ter-mar — pipeline and site tasks.
# Every target is a thin wrapper over the termar CLI so that CI, the Makefile
# and a human all run exactly the same code path.

UF ?= GO
START ?= 2021-01
END ?= 2023-12

.PHONY: setup ingest transform model emit site serve test lint typecheck validate all clean

setup:
	uv sync --all-groups

ingest:
	uv run termar ingest --uf $(UF) --start $(START) --end $(END)

transform:
	uv run termar transform --uf $(UF)

model:
	uv run termar model --start $(START) --end $(END)

emit:
	uv run termar emit --out site/data

validate:
	uv run termar validate --out site/data

site: emit validate

serve:
	python -m http.server 8000 --directory site

test:
	uv run pytest

lint:
	uv run ruff check . && uv run ruff format --check .

typecheck:
	uv run mypy

all: ingest transform model site test

clean:
	rm -rf data/interim/* data/out/* site/data/*.json site/data/serie site/data/funnel
