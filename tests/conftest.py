from __future__ import annotations
from collections.abc import Iterator
from typing import Any
import allure
import pytest
from playwright.sync_api import Page
from src.api import JsonPlaceholderClient
from src.config import Settings, get_settings
from src.pages.inventory_page import InventoryPage
from src.pages.login_page import LoginPage


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()


@pytest.fixture(scope="session")
def browser_context_args(
    browser_context_args: dict[str, object],
) -> dict[str, object]:
    return {
        **browser_context_args,
        "viewport": {
            "width": 1280,
            "height": 720,
        },
    }


@pytest.fixture
def login_page(
    page: Page,
    settings: Settings,
    request: pytest.FixtureRequest,
) -> LoginPage:
    _register_playwright_artifacts(page, request)
    return LoginPage(
        page=page,
        base_url=settings.ui_base_url,
        timeout_ms=settings.default_timeout_ms,
    )


@pytest.fixture(scope="function")
def logged_in_inventory_page(
    login_page: LoginPage, settings: Settings
) -> InventoryPage:
    return login_page.navigate().login_successfully(
        settings.swag_labs_standard_username,
        settings.swag_labs_password,
    )


@pytest.fixture
def api_client(settings: Settings) -> Iterator[JsonPlaceholderClient]:
    client = JsonPlaceholderClient(
        base_url=settings.api_base_url,
        timeout_seconds=settings.api_timeout_seconds,
    )

    yield client

    client.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[Any]):
    outcome = yield
    report = outcome.get_result()

    if report.when not in ("setup", "call") or not report.failed:
        return

    page = _get_playwright_page(item)
    if page is not None and not page.is_closed():
        _attach_failure_screenshot(page)
        _attach_page_html(page)

    _attach_browser_console_logs(item)


def _register_playwright_artifacts(
    page: Page,
    request: pytest.FixtureRequest,
) -> None:
    console_logs: list[str] = []
    setattr(request.node, "_playwright_page", page)
    setattr(request.node, "_browser_console_logs", console_logs)

    page.on(
        "console",
        lambda message: console_logs.append(f"[{message.type}] {message.text}"),
    )
    page.on("pageerror", lambda error: console_logs.append(f"[pageerror] {error}"))


def _get_playwright_page(item: pytest.Item) -> Page | None:
    stored_page = getattr(item, "_playwright_page", None)
    if isinstance(stored_page, Page):
        return stored_page

    page = item.funcargs.get("page")
    if isinstance(page, Page):
        return page

    for fixture_value in item.funcargs.values():
        fixture_page = getattr(fixture_value, "page", None)
        if isinstance(fixture_page, Page):
            return fixture_page

    return None


def _attach_failure_screenshot(page: Page) -> None:
    allure.attach(
        page.screenshot(full_page=True),
        name="failure-screenshot",
        attachment_type=allure.attachment_type.PNG,
    )


def _attach_page_html(page: Page) -> None:
    allure.attach(
        page.content(),
        name="page-dom",
        attachment_type=allure.attachment_type.HTML,
    )


def _attach_browser_console_logs(item: pytest.Item) -> None:
    console_logs = getattr(item, "_browser_console_logs", [])
    log_output = "\n".join(console_logs) if console_logs else "No browser console logs captured."

    allure.attach(
        log_output,
        name="browser-console-logs",
        attachment_type=allure.attachment_type.TEXT,
    )
