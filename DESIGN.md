# Design Notes

## Goals

This framework is intentionally small, explicit, and parallel-safe. Tests own
their setup through pytest fixtures and do not share mutable state across test
cases or workers.

## UI Automation

Swag Labs browser coverage uses the Page Object Model. Test files describe user
intent only; selectors and Playwright interactions live in `src/pages/`.

Selector rules:

- All Swag Labs selectors use `data-test` attributes.
- No `time.sleep()` calls are used.
- Synchronization relies on Playwright auto-waiting and `expect()` assertions.

## API Automation

The JSONPlaceholder client in `src/api/jsonplaceholder_client.py` centralizes:

- Base URL construction.
- Default JSON headers.
- Request timeouts.
- Connection and transport exception handling.

The client returns raw `requests.Response` objects so tests can assert both
successful and expected negative status codes, such as `404`.

While `len(posts) == 100` is appropriate for JSONPlaceholder's static data, a real-world dynamic environment should use programmatic data seeding with setup and teardown to preserve isolation and avoid data-related flakiness.

## Configuration

Runtime settings are loaded in `src/config.py` with `python-dotenv`. Defaults
make the suite runnable without local setup, while environment variables allow
CI and developer machines to override URLs, credentials, and timeouts.

Credentials and environment-specific values should come from environment
variables. Local secrets can be stored in a git-ignored `.env` file, while CI
should inject them through its secret manager.

## Parallel Execution

`pytest-xdist` is used for parallelism. UI tests use the fresh `page` fixture
provided by `pytest-playwright`, and API tests instantiate a new lightweight
client per test, keeping test execution independent.

## CI

GitHub Actions installs Python dependencies, installs Playwright browsers, runs
the full suite with two workers, and uploads both the pytest HTML report and
Playwright trace output as artifacts.
