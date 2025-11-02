# Repository Guidelines

## Project Structure & Module Organization
```
polymind/
├─ src/           # Python source code
├─ tests/         # Test suite (pytest)
├─ docs/          # Documentation assets
├─ scripts/       # Helper scripts (lint, format)
└─ requirements.txt
```
All production code lives under **src**; keep modules small and import‑friendly.  Test files mirror the package layout (e.g., `src/utils.py` → `tests/test_utils.py`).

## Build, Test, and Development Commands
| Command | Description |
|---------|-------------|
| `pip install -r requirements.txt` | Install dependencies locally |
| `make lint` | Run `ruff` linting and auto‑fixes |
| `make fmt` | Apply `ruff format` to the whole repo |
| `pytest` | Execute the test suite with coverage |
| `python -m src.main` | Run the application entry point |

## Coding Style & Naming Conventions
* **Indentation:** 4 spaces, no tabs.
* **Line length:** 88 characters (compatible with `ruff` defaults).
* **Naming:**
  * Modules & packages – `snake_case`
  * Classes – `PascalCase`
  * Functions/variables – `snake_case`
  * Constants – `UPPER_SNAKE_CASE`
* **Formatting:** Enforced by `ruff format`; run `make fmt` before committing.

## Testing Guidelines
* **Framework:** `pytest` with `pytest-cov` for coverage.
* **File naming:** `test_*.py` or `*_test.py` inside `tests/`.
* **Coverage target:** ≥ 80 % overall; ensure new code is covered.
* **Running tests:** `pytest` (or `make test` if defined).
* **Mocking:** Use `unittest.mock` for external services.

## Commit & Pull Request Guidelines
* **Commit messages:** Follow the conventional‑commits format:
  ```
  type(scope): short description

  Optional longer description.
  ```
  Types include `feat`, `fix`, `docs`, `refactor`, `test`, `chore`.
* **PR description:** Brief summary, linked issue (`Fixes #123`), and any relevant screenshots or logs.
* **Review checklist:**
  - Code passes `make lint` and `make fmt`.
  - Tests run cleanly with required coverage.
  - No new security warnings (`bandit` scan).

## Security & Configuration Tips
* Keep secrets out of source – use environment variables or a `.env.example` file.
* Run `bandit -r src` locally to spot common security issues.
* Dependencies are pinned in `requirements.txt`; update with `pip‑freeze > requirements.txt`.

---
These guidelines are intentionally concise; refer to the detailed docs in `docs/` for deeper explanations.

