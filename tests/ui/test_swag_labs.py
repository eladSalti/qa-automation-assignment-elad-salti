from __future__ import annotations
import pytest
from src.config import Settings
from src.pages.inventory_page import InventoryPage
from src.pages.login_page import LoginPage


@pytest.mark.ui
def test_login_happy_path(login_page: LoginPage,settings: Settings):
    """
    Happy path tests for login page.
    """
    inventory_page = login_page.navigate().login_successfully(
        settings.swag_labs_standard_username,
        settings.swag_labs_password,
    )

    inventory_page.expect_items_visible()


@pytest.mark.ui
def test_login_invalid_credentials(login_page: LoginPage):
    """
    Invalid credentials tests for login page.
    """
    login_page.navigate().submit_invalid_login(
        username="invalid_user",
        password="invalid_password",
    )

    login_page.expect_error_message(
        "Epic sadface: Username and password do not match any user in this service",
    )


@pytest.mark.ui
def test_add_to_cart_and_verify_state(logged_in_inventory_page: InventoryPage):
    first_product = logged_in_inventory_page.add_product_to_cart_by_index(0)
    second_product = logged_in_inventory_page.add_product_to_cart_by_index(1)
    expected_products = {
        first_product["name"]: first_product["price"],
        second_product["name"]: second_product["price"],
    }
    logged_in_inventory_page.expect_cart_badge_count(2)
    cart_page = logged_in_inventory_page.open_cart()

    cart_page.expect_loaded()
    cart_page.expect_products_present(expected_products)


@pytest.mark.ui
def test_end_to_end_checkout(logged_in_inventory_page: InventoryPage):
    """
    End to end tests for checkout page.
    """
    logged_in_inventory_page.add_product_to_cart_by_index(0)
    logged_in_inventory_page.expect_cart_badge_count(1)
    checkout_page = logged_in_inventory_page.open_cart().checkout()

    checkout_page.complete_checkout(
        first_name="Elad",
        last_name="Salti",
        postal_code="12345",
    )
    checkout_page.expect_order_complete()


@pytest.mark.ui
def test_sort_products_by_price_low_to_high(logged_in_inventory_page: InventoryPage):
    logged_in_inventory_page.sort_by_price_low_to_high()
    logged_in_inventory_page.expect_prices_sorted_low_to_high()


@pytest.mark.ui
def test_cart_badge_updates_when_items_are_added_and_removed(logged_in_inventory_page: InventoryPage):
    logged_in_inventory_page.add_product_to_cart_by_index(0)
    logged_in_inventory_page.expect_cart_badge_count(1)
    logged_in_inventory_page.add_product_to_cart_by_index(1)
    logged_in_inventory_page.expect_cart_badge_count(2)

    logged_in_inventory_page.remove_product_from_cart_by_index(0)
    logged_in_inventory_page.expect_cart_badge_count(1)
    logged_in_inventory_page.remove_product_from_cart_by_index(1)
    logged_in_inventory_page.expect_cart_badge_hidden()
