"""
Debug Dify Install Page Structure
"""
import pytest
import pytest_asyncio


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_inspect_dify_install_page(page, dify_base_url):
    """Inspect the structure of Dify install page"""
    print("\n=== Inspecting Dify Install Page ===")
    
    await page.goto(dify_base_url, timeout=30000)
    await page.wait_for_load_state("networkidle")
    await page.wait_for_timeout(3000)  # Wait longer for React to render
    
    print(f"URL: {page.url}")
    
    # Get HTML content
    html = await page.content()
    print(f"\nHTML length: {len(html)} bytes")
    
    # Get body text
    body_text = await page.inner_text("body")
    print(f"Body text: {body_text[:500]}")
    
    # Count different elements
    buttons = page.locator('button')
    inputs = page.locator('input')
    forms = page.locator('form')
    divs = page.locator('div')
    
    print(f"\nElement counts:")
    print(f"  Buttons: {await buttons.count()}")
    print(f"  Inputs: {await inputs.count()}")
    print(f"  Forms: {await forms.count()}")
    print(f"  Divs: {await divs.count()}")
    
    # Try to find any clickable elements
    clickable = page.locator('button, a, [role="button"]')
    clickable_count = await clickable.count()
    print(f"  Clickable elements: {clickable_count}")
    
    # Print first few clickable elements
    for i in range(min(clickable_count, 10)):
        text = await clickable.nth(i).inner_text()
        tag = await clickable.nth(i).evaluate("el => el.tagName")
        print(f"    {i}: <{tag}> {text[:50]}")
    
    # Take full page screenshot
    await page.screenshot(path="screenshots/dify_install_debug.png", full_page=True)
    
    # Save HTML to file for inspection
    with open("screenshots/dify_install.html", "w") as f:
        f.write(html)
    
    print("\n✓ Debug info saved to screenshots/")
