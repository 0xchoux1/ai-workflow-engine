"""
Dify Initial Setup Automation
"""
import pytest
import pytest_asyncio


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_dify_initial_setup(page, dify_base_url):
    """Complete Dify initial setup"""
    print("\n=== Starting Dify Setup ===")
    
    # Navigate to Dify
    await page.goto(dify_base_url, timeout=30000)
    await page.wait_for_load_state("networkidle")
    await page.wait_for_timeout(2000)
    
    print(f"Current URL: {page.url}")
    
    # Check if we're on the install page
    if "/install" in page.url:
        print("On install page, proceeding with setup...")
        
        # Take screenshot of install page
        await page.screenshot(path="screenshots/dify_install_page.png")
        
        # Look for email input
        email_input = page.locator('input[type="email"], input[name="email"], input[placeholder*="email" i]').first
        
        # Check if email input exists
        if await email_input.count() > 0:
            print("Found email input")
            
            # Fill in the setup form
            await email_input.fill("admin@example.com")
            await page.wait_for_timeout(500)
            
            # Look for name input
            name_input = page.locator('input[type="text"], input[name="name"], input[placeholder*="name" i]').first
            if await name_input.count() > 0:
                print("Found name input")
                await name_input.fill("Admin User")
                await page.wait_for_timeout(500)
            
            # Look for password input
            password_inputs = page.locator('input[type="password"]')
            password_count = await password_inputs.count()
            print(f"Found {password_count} password inputs")
            
            if password_count > 0:
                # Fill password
                await password_inputs.nth(0).fill("Admin123456!")
                await page.wait_for_timeout(500)
                
                # If there's a confirm password field
                if password_count > 1:
                    await password_inputs.nth(1).fill("Admin123456!")
                    await page.wait_for_timeout(500)
            
            # Take screenshot before submit
            await page.screenshot(path="screenshots/dify_setup_filled.png")
            
            # Look for submit button (case-insensitive)
            submit_button = page.locator('button:has-text("Set up")').first
            
            if await submit_button.count() > 0:
                print("Found submit button, clicking...")
                await submit_button.click()
                
                # Wait for navigation
                await page.wait_for_timeout(3000)
                await page.wait_for_load_state("networkidle")
                
                print(f"After submit URL: {page.url}")
                await page.screenshot(path="screenshots/dify_after_setup.png")
                
                # Check if setup was successful (should redirect away from /install)
                assert "/install" not in page.url, "Still on install page after setup"
                print("✓ Setup completed successfully!")
            else:
                print("Could not find submit button")
                # Get page content for debugging
                content = await page.content()
                print(f"Page content length: {len(content)}")
        else:
            print("Could not find email input field")
            # Try to find any input fields
            all_inputs = page.locator('input')
            input_count = await all_inputs.count()
            print(f"Total input fields found: {input_count}")
            
            # Print all input field info
            for i in range(min(input_count, 5)):
                input_type = await all_inputs.nth(i).get_attribute('type')
                input_name = await all_inputs.nth(i).get_attribute('name')
                input_placeholder = await all_inputs.nth(i).get_attribute('placeholder')
                print(f"  Input {i}: type={input_type}, name={input_name}, placeholder={input_placeholder}")
    else:
        print(f"Not on install page, already setup? Current URL: {page.url}")
        await page.screenshot(path="screenshots/dify_main_page.png")


@pytest.mark.e2e
@pytest.mark.asyncio  
async def test_dify_login_after_setup(page, dify_base_url):
    """Test login to Dify after setup"""
    print("\n=== Testing Dify Login ===")
    
    await page.goto(dify_base_url, timeout=30000)
    await page.wait_for_load_state("networkidle")
    await page.wait_for_timeout(2000)
    
    print(f"Current URL: {page.url}")
    
    # If on login page
    if "/signin" in page.url or "/login" in page.url:
        print("On login page")
        
        # Try to login with setup credentials
        email_input = page.locator('input[type="email"], input[name="email"]').first
        password_input = page.locator('input[type="password"]').first
        
        if await email_input.count() > 0 and await password_input.count() > 0:
            await email_input.fill("admin@example.com")
            await password_input.fill("Admin123456!")
            
            login_button = page.locator('button[type="submit"], button:has-text("Sign in"), button:has-text("Login")').first
            if await login_button.count() > 0:
                await login_button.click()
                await page.wait_for_timeout(3000)
                await page.wait_for_load_state("networkidle")
                
                print(f"After login URL: {page.url}")
                await page.screenshot(path="screenshots/dify_logged_in.png")
    else:
        print("Not on login page")
        await page.screenshot(path="screenshots/dify_current_state.png")
