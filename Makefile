.PHONY: lint format format-check typecheck djlint \
        js-format js-format-check \
        check fix test

PYTHON_SRC := app tests
TEMPLATES := app/templates
JS_CSS := assets

# -------------------------
# Python
# -------------------------

lint:
	uv run ruff check $(PYTHON_SRC)

format:
	uv run ruff format $(PYTHON_SRC)

format-check:
	uv run ruff format --check $(PYTHON_SRC)

typecheck:
	uv run ty check $(PYTHON_SRC)

test:
	uv run pytest

# -------------------------
# Templates
# -------------------------

djlint:
	uv run djlint $(TEMPLATES)

# -------------------------
# JavaScript / CSS
# -------------------------

js-format:
	npx prettier --write $(JS_CSS)

js-format-check:
	npx prettier --check $(JS_CSS)

# -------------------------
# Everything
# -------------------------

check:
	@printf '\n==> Python: linting\n'
	uv run ruff check $(PYTHON_SRC)

	@printf '\n==> Python: checking formatting\n'
	uv run ruff format --check $(PYTHON_SRC)

	@printf '\n==> Python: type checking\n'
	uv run ty check $(PYTHON_SRC)

	@printf '\n==> Templates: checking with djlint\n'
	uv run djlint $(TEMPLATES)

	@printf '\n==> JavaScript / CSS: checking formatting\n'
	npx prettier --check $(JS_CSS)

	@printf '\n✓ All checks passed!\n'

fix:
	@printf '\n==> Python: linting and formatting\n'
	uv run ruff check --fix $(PYTHON_SRC)
	uv run ruff format $(PYTHON_SRC)

	@printf '\n==> Templates: formatting with djlint\n'
	uv run djlint $(TEMPLATES) --reformat

	@printf '\n==> JavaScript / CSS: formatting with Prettier\n'
	npx prettier --write $(JS_CSS)

	@printf '\n✓ Formatting complete!\n'
