import pytest

@pytest.fixture(scope="module")
def test_endpoint():
        return "https://www.google.com/"

@pytest.mark.asyncio
async def test_async_driver(test_endpoint):
        from chromex.chromex import driver
        from chromex.models.driver import ChromeX, Chrome

        # Test driver method
        chrome = await driver()
        assert isinstance(chrome._browser, Chrome)
        assert isinstance(chrome, ChromeX)
        
        # Test get method
        await chrome.get(test_endpoint)

        assert chrome._browser.current_url == test_endpoint
