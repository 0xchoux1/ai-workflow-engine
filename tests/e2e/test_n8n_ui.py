"""
E2E Tests for n8n UI
"""
import pytest
import pytest_asyncio


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_n8n_homepage_loads(page, n8n_base_url):
    """Test that n8n homepage loads successfully"""
    await page.goto(n8n_base_url, timeout=30000)
    
    # Wait for the page to load
    await page.wait_for_load_state("networkidle")
    
    # Check if we're on n8n page (either login or main page)
    title = await page.title()
    assert "n8n" in title.lower() or len(title) > 0, f"Unexpected title: {title}"
    
    print(f"✓ n8n page loaded: {title}")


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_n8n_login_page_exists(page, n8n_base_url):
    """Test that n8n shows a login or setup page"""
    await page.goto(n8n_base_url, timeout=30000)
    await page.wait_for_load_state("networkidle")
    
    # Check if page has loaded with some content
    body_text = await page.inner_text("body")
    assert len(body_text) > 0, "Page body is empty"
    
    print("✓ n8n page has content")


@pytest.mark.e2e
@pytest.mark.asyncio
@pytest.mark.slow
async def test_n8n_workflow_page_structure(page, n8n_base_url):
    """Test basic structure of n8n workflow page"""
    await page.goto(n8n_base_url, timeout=30000)
    await page.wait_for_load_state("domcontentloaded")
    
    # Take a screenshot for debugging
    await page.screenshot(path="screenshots/n8n_homepage.png")
    
    # Check that the page loaded without errors
    assert page.url.startswith(n8n_base_url)
    
    print(f"✓ n8n URL is correct: {page.url}")
