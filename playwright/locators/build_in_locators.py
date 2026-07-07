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
class TestBuildInLocators:
    def test_get_by_role(self):
        first_name = self.page.get_by_role("textbox", name="First Name")
        first_name.fill("Sajjad")
        time.sleep(3)

        self.page.get_by_role("checkbox", name="Newsletter").check()
        time.sleep(3)

        self.page.get_by_role("radio", name="WhatsApp").check()
        time.sleep(3)

        self.page.get_by_role("button", name="Final Submission").click()
        time.sleep(3)

        self.page.get_by_role("link", name="Back").click()
        time.sleep(3)

    def test_get_by_label(self):
        self.page.get_by_label("First Name").fill("Sajjad")
        time.sleep(3)
        self.page.get_by_label("Personal Email").fill("test@noemail.com")
        time.sleep(3)
        self.page.get_by_label("Marital Status").select_option("Married")
        time.sleep(3)