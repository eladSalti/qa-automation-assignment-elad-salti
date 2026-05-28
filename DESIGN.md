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

Core application values, such as URLs, timeouts, and credentials, are
externalized through `src/config.py`. Framework execution settings follow native
pytest tooling conventions: browser selection is centralized in `pytest.ini`
with `--browser chromium`, while CI parallelism is controlled by `pytest-xdist`
through the workflow command `pytest -n 2`.

## Parallel Execution

`pytest-xdist` is used for parallelism. UI tests use the fresh `page` fixture
provided by `pytest-playwright`, and API tests instantiate a new lightweight
client per test, keeping test execution independent.

## CI

GitHub Actions installs Python dependencies, installs Playwright browsers, runs
the full suite with two workers, publishes the Allure Report to GitHub Pages,
and uploads Allure results plus Playwright failure artifacts.

## Question 1
Language and framework choice. Why this stack? Why Playwright vs Selenium (or vice versa)? In what situation would you pick the other one?
## Answer 1
- We chose Python because it is readable, fast to develop, and a leader in the fields of Automation and Data.
- We chose Playwright because it is modern, significantly faster than Selenium, features built-in auto-waiting (which reduces flakiness), and runs parallel tests incredibly well using Workers.
- When would we choose Selenium? Only if we were required to support legacy browsers (like old Internet Explorer)

## Question 2
Anti-flakiness strategy. What concrete techniques did you use to drive flakiness toward zero? What would you add at scale (1000+ tests)?
## Answer 2
- In the current project we utilized Playwright's auto-waiting mechanisms (Locator assertions), separated configurations into a configuration file, and implemented the POM to prevent code duplication.
- At scale (1,000+ tests) We would add an automatic retry mechanism (re-running only failed tests), execute tests on an isolated Docker infrastructure, and implement a flakiness monitoring tool (such as automatically tagging problematic tests).

## Question 3
Parallelism and isolation. How are tests isolated? What breaks first when you turn parallelism up?
## Answer 3
- Isolation: The tests are isolated thanks to Playwright's BrowserContext (each test gets its own completely clean cookies and session, just like a new incognito window), and thanks to the pytest-xdist plugin, which manages a separate process for each worker.
- What breaks first at high scale: The bottleneck will either be the server's CPU (the GitHub Actions Runner), or user collisions/crashes in the DB (if multiple tests try to edit the exact same user at the exact same time - Race Conditions).

## Question 4
Reporting and triage. If a test fails in CI at 3am, what does the on-call engineer see, and what is the path to the root cause?
## Answer 4
The on-call engineer receives an alert from GitHub (or Slack). They click the link to our live Allure Report.
There, they can see exactly which step failed, get a clear Error Message (e.g., a failed Assertion), and view the attached screenshot, page DOM, browser console logs, and Playwright trace for root-cause analysis.

## Question 5
What you would do next. If you had another two days, what is the next thing you would build, and why? (We pay attention to this answer.)
## Answer 5
- I would add Visual Regression Testing for components using a tool like Applitools or Playwright's built-in screenshot comparison, to ensure the site's design does not break.
- I would create a quick Sanity test suite (using Pytest Markers) so it can be run within 20 seconds on every Pull Request, leaving the heavy test suites for the nightly run.
- Integrating basic Performance Metrics testing for the core UI pages.