from __future__ import annotations
from playwright.sync_api import expect
from src.pages.base_page import BasePage
from src.pages.inventory_page import InventoryPage


class LoginPage(BasePage):
    """Actions and assertions for the Swag Labs login page."""

    def navigate(self) -> "LoginPage":
        self.goto("/")
        expect(self.by_data_test("login-button")).to_be_visible()
        return self

    def login_successfully(self, username: str, password: str) -> InventoryPage:
        self._fill_credentials(username, password)
        self.by_data_test("login-button").click()

        error = self.by_data_test("error")
        first_inventory_item = self.by_data_test("inventory-item").first
        expect(first_inventory_item.or_(error)).to_be_visible()

        if error.is_visible():
            raise AssertionError(
                "Expected successful login, but Swag Labs displayed an error: "
                f"{error.inner_text()}"
            )

        inventory_page = InventoryPage(self.page, self.base_url, self.timeout_ms)
        inventory_page.expect_loaded()
        return inventory_page

    def submit_invalid_login(self, username: str, password: str) -> None:
        self._fill_credentials(username, password)
        self.by_data_test("login-button").click()

    def expect_error_message(self, expected_message: str) -> None:
        error = self.by_data_test("error")

        expect(error).to_be_visible()
        expect(error).to_have_text(expected_message)

    def _fill_credentials(self, username: str, password: str) -> None:
        self.by_data_test("username").fill(username)
        self.by_data_test("password").fill(password)
