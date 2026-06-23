import pytest
from playwright.sync_api import sync_playwright

#Step 1: Choose Browser / Supported browser
SUPPORTED_BROWSERS = ['firefox', 'chromium', 'webkit']

#Step 2: Define the browser
BROWSER_NAME = 'chromium'

#Step 3: URL
URL = 'https://www.google.com'

#Step 4: Setup + Teardown
@pytest.fixture(scope='class')
def setup(request):
    print(f'Starting browser {BROWSER_NAME} ...')

    #Step 5: Start Playwright
    playwright = sync_playwright().start()

    #Step 6: Launch the browser
    if BROWSER_NAME == 'chromium':
        browser = playwright.chromium.launch(headless=False)
    elif BROWSER_NAME == 'firefox':
        browser = playwright.firefox.launch(headless=False)
    elif BROWSER_NAME == 'webkit':
        browser = playwright.webkit.launch(headless=False)
    else:
        raise ValueError(f'Browser {BROWSER_NAME} not supported')

    #Step 7: Create browser context
    context = browser.new_context()

    #Step 8: Create a new page
    page = context.new_page()

    #Step 9: Open the URL
    page.goto(URL)

    request.cls.page = page

    #YIELD = Tests Run Here......
    yield

    #Teardown
    context.close()
    page.close()
    playwright.stop()


@pytest.mark.usefixtures('setup')
class TestCurrentURL:
    def test_current_url(self):
        self.page.wait_for_timeout(2000)
        currentURL = self.page.url
        print(f'Retrieved Current URL: {currentURL}')
