from playwright.sync_api import sync_playwright
import time

def test_login_logout():
    with sync_playwright() as p:
        # slow_mo=1000 means 1 second delay between actions
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        page.goto("https://www.saucedemo.com")
        time.sleep(2)  # Wait 2 seconds

        # Login steps
        page.fill('input[id="user-name"]', "standard_user")
        time.sleep(1)
        page.fill('input[id="password"]', "secret_sauce")
        time.sleep(1)
        page.click('input[id="login-button"]')
        time.sleep(2)
        assert "Products" in page.content()

        # Logout steps
        page.click('button[id="react-burger-menu-btn"]')  # Open menu
        time.sleep(2)
        page.click('a[id="logout_sidebar_link"]')         # Click logout
        time.sleep(2)

        browser.close()

if __name__ == "__main__":
    test_login_logout()