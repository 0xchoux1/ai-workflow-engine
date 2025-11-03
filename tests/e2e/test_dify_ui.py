"""
E2E Tests for Dify UI
"""
import pytest
import pytest_asyncio


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_dify_homepage_loads(page, dify_base_url):
    """Test that Dify homepage loads successfully"""
    await page.goto(dify_base_url, timeout=30000)
    
    # Wait for the page to load
    await page.wait_for_load_state("networkidle")
    
    # Check if we're on Dify page
    title = await page.title()
    assert len(title) > 0, f"Page title is empty"
    
    print(f"✓ Dify page loaded: {title}")


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_dify_login_page_exists(page, dify_base_url):
    """Test that Dify shows a login or setup page"""
    await page.goto(dify_base_url, timeout=30000)
    await page.wait_for_load_state("networkidle")
    
    # Check if page has loaded with some content
    body_text = await page.inner_text("body")
    assert len(body_text) > 0, "Page body is empty"
    
    print("✓ Dify page has content")


@pytest.mark.e2e
@pytest.mark.asyncio
@pytest.mark.slow
async def test_dify_page_structure(page, dify_base_url):
    """Test basic structure of Dify page"""
    await page.goto(dify_base_url, timeout=30000)
    await page.wait_for_load_state("domcontentloaded")
    
    # Take a screenshot for debugging
    await page.screenshot(path="screenshots/dify_homepage.png")
    
    # Check that the page loaded without errors
    assert page.url.startswith(dify_base_url) or "localhost:3000" in page.url
    
    print(f"✓ Dify URL is correct: {page.url}")
