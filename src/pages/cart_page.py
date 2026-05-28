from __future__ import annotations
from dataclasses import dataclass
from playwright.sync_api import expect
from src.pages.base_page import BasePage


@dataclass(frozen=True)
class CartItem:
    """Cart item details extracted from the UI."""

    name: str
    price: str


class CartPage(BasePage):
    """Actions and assertions for the shopping cart page."""

    def expect_loaded(self) -> None:
        self.expect_url_contains("/cart.html")
        expect(self.by_data_test("title")).to_have_text("Your Cart")

    def expect_products_present(self, expected_products: dict[str, str]) -> None:
        expect(self.by_data_test("inventory-item")).to_have_count(
            len(expected_products),
        )

        actual_products = {
            cart_item.name: cart_item.price for cart_item in self.get_cart_items()
        }

        assert actual_products == expected_products, f"Cart mismatch: expected {expected_products}, got {actual_products}"

    def get_cart_items(self) -> list[CartItem]:
        items = self.by_data_test("inventory-item")
        cart_items: list[CartItem] = []

        for index in range(items.count()):
            item = items.nth(index)
            name = item.locator('[data-test="inventory-item-name"]').inner_text()
            price = item.locator('[data-test="inventory-item-price"]').inner_text()
            cart_items.append(CartItem(name=name, price=price))

        return cart_items

    def checkout(self) -> "CheckoutPage":
        from src.pages.checkout_page import CheckoutPage

        self.by_data_test("checkout").click()
        return CheckoutPage(self.page, self.base_url, self.timeout_ms)
