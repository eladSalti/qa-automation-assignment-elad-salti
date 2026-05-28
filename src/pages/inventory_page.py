from __future__ import annotations

from playwright.sync_api import expect

from src.pages.base_page import BasePage

class InventoryPage(BasePage):
    """Actions and assertions for the products inventory page."""

    def expect_loaded(self) -> None:
        self.expect_url_contains("/inventory.html")
        expect(self.by_data_test("title")).to_have_text("Products")
        expect(self.by_data_test("inventory-item").first).to_be_visible()

    def expect_items_visible(self) -> None:
        expect(self.by_data_test("inventory-item")).to_have_count(6)

    def add_product_to_cart_by_index(self, index: int) -> dict[str, str]:
        item = self.by_data_test("inventory-item").nth(index)
        expect(item).to_be_visible()

        product_data = {
            "name": item.locator('[data-test="inventory-item-name"]').inner_text(),
            "price": item.locator('[data-test="inventory-item-price"]').inner_text(),
        }
        item.locator('[data-test^="add-to-cart"]').click()
        expect(item.locator('[data-test^="remove"]')).to_be_visible()
        return product_data

    def remove_product_from_cart_by_index(self, index: int) -> None:
        item = self.by_data_test("inventory-item").nth(index)
        expect(item).to_be_visible()
        item.locator('[data-test^="remove"]').click()
        expect(item.locator('[data-test^="add-to-cart"]')).to_be_visible()

    def sort_by_price_low_to_high(self) -> None:
        self.by_data_test("product-sort-container").select_option("lohi")

    def expect_prices_sorted_low_to_high(self) -> None:
        prices = [
            self._parse_price(price)
            for price in self.by_data_test("inventory-item-price").all_inner_texts()
        ]

        assert prices == sorted(prices), (
            f"Expected product prices to be sorted low to high, but got {prices}"
        )

    def expect_cart_badge_count(self, expected_count: int) -> None:
        expect(self.by_data_test("shopping-cart-badge")).to_have_text(
            str(expected_count),
        )

    def expect_cart_badge_hidden(self) -> None:
        expect(self.by_data_test("shopping-cart-badge")).to_be_hidden()

    def open_cart(self) -> "CartPage":
        from src.pages.cart_page import CartPage

        self.by_data_test("shopping-cart-link").click()
        return CartPage(self.page, self.base_url, self.timeout_ms)

    @staticmethod
    def _parse_price(price: str) -> float:
        return float(price.replace("$", ""))
