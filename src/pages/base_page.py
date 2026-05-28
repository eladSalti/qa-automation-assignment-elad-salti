from __future__ import annotations
import re
from playwright.sync_api import Locator, Page, expect


class BasePage:
    """Common wrapper around Playwright's page with data-test selectors."""

    def __init__(self, page: Page, base_url: str, timeout_ms: int) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/")
        self.timeout_ms = timeout_ms
        self.page.set_default_timeout(timeout_ms)

    def by_data_test(self, test_id: str) -> Locator:
        """Locate an element using only the Swag Labs data-test attribute."""

        return self.page.locator(f'[data-test="{test_id}"]')

    def goto(self, path: str = "") -> None:
        """Navigate to a path relative to the configured UI base URL."""

        normalized_path = path if path.startswith("/") else f"/{path}"
        self.page.goto(f"{self.base_url}{normalized_path}")

    def expect_url_contains(self, expected_path: str) -> None:
        """Assert the current browser URL contains the expected route."""

        url_pattern = re.compile(f".*{re.escape(expected_path)}.*")
        expect(self.page).to_have_url(url_pattern)
