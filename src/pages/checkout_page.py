from __future__ import annotations
from playwright.sync_api import expect
from src.pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Actions and assertions for the checkout journey."""

    def complete_checkout(
        self,
        first_name: str,
        last_name: str,
        postal_code: str,
    ) -> None:
        self.fill_customer_information(first_name, last_name, postal_code)
        self.finish_order()

    def fill_customer_information(
        self,
        first_name: str,
        last_name: str,
        postal_code: str,
    ) -> None:
        self.expect_url_contains("/checkout-step-one.html")
        expect(self.by_data_test("title")).to_have_text("Checkout: Your Information")

        self.by_data_test("firstName").fill(first_name)
        self.by_data_test("lastName").fill(last_name)
        self.by_data_test("postalCode").fill(postal_code)
        self.by_data_test("continue").click()

        self.expect_url_contains("/checkout-step-two.html")
        expect(self.by_data_test("title")).to_have_text("Checkout: Overview")

    def finish_order(self) -> None:
        self.by_data_test("finish").click()
        self.expect_url_contains("/checkout-complete.html")

    def expect_order_complete(self) -> None:
        expect(self.by_data_test("complete-header")).to_have_text(
            "Thank you for your order!",
        )
        expect(self.by_data_test("complete-text")).to_have_text(
            "Your order has been dispatched, and will arrive just as fast as the "
            "pony can get there!",
        )
