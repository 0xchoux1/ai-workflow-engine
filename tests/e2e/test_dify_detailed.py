"""
Detailed E2E Tests for Dify UI
"""
import pytest
import pytest_asyncio


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_dify_page_loads_with_content(page, dify_base_url):
    """Test that Dify page loads with actual content"""
    # Navigate to Dify
    await page.goto(dify_base_url, timeout=30000)
    
    # Wait for network to be idle
    await page.wait_for_load_state("networkidle")
    
    # Wait a bit more for JavaScript to render
    await page.wait_for_timeout(2000)
    
    # Take screenshot
    await page.screenshot(path="screenshots/dify_detailed.png", full_page=True)
    
    # Get page content
    content = await page.content()
    
    # Check if page has meaningful content
    assert len(content) > 1000, f"Page content too small: {len(content)} bytes"
    
    # Check for common elements
    title = await page.title()
    print(f"Page title: {title}")
    print(f"Content length: {len(content)} bytes")
    print(f"URL: {page.url}")
    
    # Get all text content
    body_text = await page.inner_text("body")
    print(f"Body text length: {len(body_text)} chars")
    
    assert len(body_text) > 0, "Body text is empty"


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_dify_check_elements(page, dify_base_url):
    """Check if Dify has specific UI elements"""
    await page.goto(dify_base_url, timeout=30000)
    await page.wait_for_load_state("domcontentloaded")
    await page.wait_for_timeout(2000)
    
    # Check for any visible elements
    html = await page.inner_html("html")
    print(f"HTML length: {len(html)} bytes")
    
    # Look for common patterns
    has_react = "react" in html.lower()
    has_vue = "vue" in html.lower()
    has_next = "next" in html.lower() or "_next" in html
    
    print(f"React detected: {has_react}")
    print(f"Vue detected: {has_vue}")
    print(f"Next.js detected: {has_next}")
    
    # At least one should be present for a modern web app
    assert has_react or has_vue or has_next or len(html) > 5000, \
        "Page doesn't seem to have loaded properly"
