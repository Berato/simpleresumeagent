from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class BrowserService:
    def __init__(self):
        self._playwright = None
        self._browser: Optional[Browser] = None

    async def start(self):
        """Initialize the global browser instance"""
        if not self._browser:
            logger.info("Starting global browser instance...")
            self._playwright = await async_playwright().start()
            self._browser = await self._playwright.chromium.launch(headless=True)

    async def stop(self):
        """Close the global browser instance"""
        if self._browser:
            logger.info("Closing global browser instance...")
            await self._browser.close()
            await self._playwright.stop()
            self._browser = None
            self._playwright = None

    async def fetch_html(self, url: str, wait_until: str = "networkidle") -> str:
        """Fetch rendered HTML from a URL"""
        if not self._browser:
            await self.start()
        
        context: BrowserContext = await self._browser.new_context()
        page: Page = await context.new_page()
        try:
            logger.info(f"Fetching URL: {url}")
            await page.goto(url, wait_until=wait_until)
            # Short extra wait for safety if needed, or specific selectors
            content = await page.content()
            return content
        finally:
            await page.close()
            await context.close()

# Global instance
browser_service = BrowserService()
