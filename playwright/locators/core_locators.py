import time
import pytest
from playwright.sync_api import sync_playwright

#Step 1: Choose Browser / Supported browser
SUPPORTED_BROWSERS = ["chromium", "firefox", "webkit"]
# Step 2: Define the browser
BROWSER_NAME = "chromium"
#Step 3: URL
URL = "https://automation.ebrahimhossain.com.bd/form.html"

#Step 4: Setup + Teardown
@pytest.fixture(scope="class")
def setup(request):
    print(f"Starting {BROWSER_NAME} browser....")
    # Step 5: Start Playwright
    playwright = sync_playwright().start()
    #Step 6: Launch the browser
    if BROWSER_NAME == "chromium":
        browser = playwright.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
        )
    elif BROWSER_NAME == "firefox":
        browser = playwright.firefox.launch(headless=False)
    elif BROWSER_NAME == "webkit":
        browser = playwright.webkit.launch(headless=False)
    else:
        raise ValueError(f"Browser {BROWSER_NAME} is not supported.")

    # Step 7: create browser context
    context = browser.new_context()
    #Step 8: Create a new page
    page = context.new_page()
    # Viewport - Screen Size
    page.set_viewport_size({"width": 1920, "height": 1080})
    #Step 9: Open the URL
    page.goto(URL)
    request.cls.page = page

    # YIELD = Tests Run Here.....
    yield
    # Teardown
    context.close()
    browser.close()
    playwright.stop()


@pytest.mark.usefixtures("setup")
class TestCoreLocators:
    """Locating by ID"""
    def test_by_id(self):
        first_name = self.page.locator('#firstName')  # For Class -> Dot(.), For Id -> #
        first_name.fill('Sajjad')
        time.sleep(2)

    def test_by_name(self):
        nid = self.page.locator("[name='national_id']")
        nid.fill('1234567890')
        time.sleep(2)

    def test_by_css_selector(self):
        # tagName[attributeName='value']
        last_name = self.page.locator("input[name='last_name']")
        last_name.fill("Hossain")
        time.sleep(2)

    def test_by_class(self):
        emergency_call = self.page.locator(".form-input").nth(4)
        emergency_call.fill("10125")
        time.sleep(2)

    def test_by_class2(self):
        dropdown = self.page.locator(".form-select").nth(1)
        dropdown.click()
        time.sleep(2)