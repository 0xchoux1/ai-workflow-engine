"""
E2E Test Configuration for Playwright
"""
import pytest
import pytest_asyncio
import asyncio
from playwright.async_api import async_playwright


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the session"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def playwright_instance():
    """Launch Playwright instance"""
    async with async_playwright() as p:
        yield p


@pytest_asyncio.fixture(scope="session")
async def browser(playwright_instance):
    """Launch browser for E2E tests"""
    browser = await playwright_instance.chromium.launch(headless=True)
    yield browser
    await browser.close()


@pytest_asyncio.fixture
async def context(browser):
    """Create a new context for each test"""
    context = await browser.new_context()
    yield context
    await context.close()


@pytest_asyncio.fixture
async def page(context):
    """Create a new page for each test"""
    page = await context.new_page()
    yield page
    await page.close()


@pytest.fixture
def n8n_base_url():
    """n8n base URL"""
    return "http://localhost:5678"


@pytest.fixture
def dify_base_url():
    """Dify base URL"""
    return "http://localhost:3000"
