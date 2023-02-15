import asyncio
import pytest

@pytest.fixture(scope="module")
def test_endpoint():
        return "https://www.google.com/"

@pytest.mark.asyncio
async def test_async_driver(test_endpoint):
        from chromex.driver import async_driver
        browser = await async_driver()
        
        # Test get method
        await browser.get(test_endpoint)
        assert browser._driver.current_url == test_endpoint