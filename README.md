# 🧪 qa-automation-assignment-elad-salti

[![Playwright Tests](https://github.com/eladSalti/qa-automation-assignment-elad-salti/actions/workflows/tests.yml/badge.svg)](https://github.com/eladSalti/qa-automation-assignment-elad-salti/actions)

### 📊 Live Test Report
You can view the interactive Allure test report, complete with execution history and failure screenshots, here:
👉 **[View Live Allure Report](https://eladSalti.github.io/qa-automation-assignment-elad-salti/)**

---

Production-grade sample automation framework for UI and API testing.

## Stack

- Python 3.11+
- Playwright sync API with `pytest-playwright`
- `requests` for API testing
- `pytest` with `pytest-xdist` for parallel execution
- Allure for test reporting
- `python-dotenv` for environment configuration

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install --with-deps
```

## Configuration

Defaults are defined in `src/config.py` and can be overridden with environment
variables or a local `.env` file:

```bash
UI_BASE_URL=https://www.saucedemo.com/
API_BASE_URL=https://jsonplaceholder.typicode.com/
DEFAULT_TIMEOUT_MS=10000
API_TIMEOUT_SECONDS=10
SWAG_LABS_STANDARD_USERNAME=standard_user
SWAG_LABS_PASSWORD=secret_sauce
```

Do not commit real credentials. For local runs, store sensitive values in a
git-ignored `.env` file. In CI, inject them through the CI secret manager, such
as GitHub Actions secrets.

## Running Tests

```bash
pytest
pytest -m ui
pytest -m api
pytest -n 2 --screenshot=only-on-failure --tracing=retain-on-failure --alluredir=allure-results
```

## Project Layout

- `src/config.py`: centralized environment-driven settings.
- `src/pages/`: Swag Labs page objects using only `data-test` selectors.
- `src/api/`: thin JSONPlaceholder API client wrapper.
- `tests/ui/`: UI scenario tests.
- `tests/api/`: API scenario tests.
- `.github/workflows/tests.yml`: CI pipeline for push and pull requests.
