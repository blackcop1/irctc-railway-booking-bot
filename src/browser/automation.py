"""Browser automation using Playwright for IRCTC booking"""

import asyncio
from typing import Optional, Dict, Any, List, Sequence
from playwright.async_api import (
    async_playwright,
    Page,
    Browser,
    BrowserContext,
    TimeoutError as PlaywrightTimeoutError,
    ElementHandle,
)
from ..utils.logger import setup_logger
from ..utils.constants import (
    DEFAULT_VIEWPORT_WIDTH,
    DEFAULT_VIEWPORT_HEIGHT,
    USER_AGENT,
    BOOKING_TIMEOUT,
    DEFAULT_PAGE_TIMEOUT,
)

logger = setup_logger(__name__)


class BrowserAutomation:
    """Automate browser interactions for IRCTC booking"""

    def __init__(
        self,
        headless: bool = False,
        viewport_width: int = DEFAULT_VIEWPORT_WIDTH,
        viewport_height: int = DEFAULT_VIEWPORT_HEIGHT,
        timeout: int = DEFAULT_PAGE_TIMEOUT,
    ):
        """Initialize browser automation
        
        Args:
            headless: Run browser in headless mode
            viewport_width: Browser viewport width
            viewport_height: Browser viewport height
            timeout: Page timeout in milliseconds
        """
        self.headless = headless
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height
        self.timeout = timeout * 1000  # Convert to milliseconds
        
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.playwright = None
    
    async def launch(self, browser_type: str = "chromium") -> None:
        """Launch browser
        
        Args:
            browser_type: Browser type (chromium, firefox, webkit)
        """
        try:
            self.playwright = await async_playwright().start()
            
            if browser_type == "chromium":
                browser_factory = self.playwright.chromium
            elif browser_type == "firefox":
                browser_factory = self.playwright.firefox
            elif browser_type == "webkit":
                browser_factory = self.playwright.webkit
            else:
                raise ValueError(f"Unsupported browser type: {browser_type}")
            
            self.browser = await browser_factory.launch(headless=self.headless)
            logger.info(f"Browser {browser_type} launched (headless={self.headless})")
        
        except Exception as e:
            logger.error(f"Failed to launch browser: {e}")
            raise
    
    async def create_context(self) -> None:
        """Create browser context"""
        if not self.browser:
            raise RuntimeError("Browser not launched. Call launch() first.")
        
        try:
            self.context = await self.browser.new_context(
                viewport={"width": self.viewport_width, "height": self.viewport_height},
                user_agent=USER_AGENT,
            )
            logger.info("Browser context created")
        
        except Exception as e:
            logger.error(f"Failed to create context: {e}")
            raise
    
    async def create_page(self) -> Page:
        """Create new page
        
        Returns:
            Page instance
        """
        if not self.context:
            raise RuntimeError("Context not created. Call create_context() first.")
        
        try:
            self.page = await self.context.new_page()
            self.page.set_default_timeout(self.timeout)
            self.page.set_default_navigation_timeout(self.timeout)
            logger.info("New page created")
            return self.page
        
        except Exception as e:
            logger.error(f"Failed to create page: {e}")
            raise
    
    async def goto(self, url: str) -> None:
        """Navigate to URL
        
        Args:
            url: Target URL
        """
        if not self.page:
            raise RuntimeError("Page not created. Call create_page() first.")
        
        try:
            await self.page.goto(url, wait_until="networkidle")
            logger.info(f"Navigated to {url}")
        
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {e}")
            raise

    async def wait_for_any(
        self,
        selectors: Sequence[str],
        timeout_ms: Optional[int] = None,
    ) -> str:
        """Wait for first available selector and return it."""
        if not self.page:
            raise RuntimeError("Page not created")

        timeout = timeout_ms if timeout_ms is not None else self.timeout
        last_error = None

        for selector in selectors:
            try:
                await self.page.wait_for_selector(selector, timeout=timeout)
                return selector
            except Exception as exc:
                last_error = exc

        raise PlaywrightTimeoutError(
            f"None of selectors matched within timeout: {selectors}"
        ) from last_error
    
    async def fill_input(self, selector: str, value: str) -> None:
        """Fill input field
        
        Args:
            selector: CSS selector
            value: Input value
        """
        if not self.page:
            raise RuntimeError("Page not created")
        
        try:
            await self.page.fill(selector, value)
            logger.debug(f"Filled {selector} with value")
        
        except Exception as e:
            logger.error(f"Failed to fill {selector}: {e}")
            raise

    async def fill_any(self, selectors: Sequence[str], value: str) -> str:
        """Fill first matching selector from candidates."""
        selector = await self.wait_for_any(selectors)
        await self.fill_input(selector, value)
        return selector
    
    async def click(self, selector: str) -> None:
        """Click element
        
        Args:
            selector: CSS selector
        """
        if not self.page:
            raise RuntimeError("Page not created")
        
        try:
            await self.page.click(selector)
            logger.debug(f"Clicked {selector}")
        
        except Exception as e:
            logger.error(f"Failed to click {selector}: {e}")
            raise

    async def click_any(self, selectors: Sequence[str]) -> str:
        """Click first matching selector from candidates."""
        selector = await self.wait_for_any(selectors)
        await self.click(selector)
        return selector
    
    async def get_text(self, selector: str) -> str:
        """Get element text
        
        Args:
            selector: CSS selector
        
        Returns:
            Element text content
        """
        if not self.page:
            raise RuntimeError("Page not created")
        
        try:
            text = await self.page.text_content(selector)
            return text or ""
        
        except Exception as e:
            logger.error(f"Failed to get text from {selector}: {e}")
            raise

    async def get_text_any(self, selectors: Sequence[str]) -> str:
        """Read text from first matching selector from candidates."""
        selector = await self.wait_for_any(selectors)
        return await self.get_text(selector)

    async def query_all_any(
        self, selectors: Sequence[str]
    ) -> tuple[str, List[ElementHandle]]:
        """Return elements for first selector that yields any nodes."""
        if not self.page:
            raise RuntimeError("Page not created")

        for selector in selectors:
            try:
                elements = await self.page.query_selector_all(selector)
                if elements:
                    return selector, elements
            except Exception:
                continue
        return "", []

    async def exists_any(self, selectors: Sequence[str]) -> bool:
        """Check if any selector exists in DOM."""
        if not self.page:
            raise RuntimeError("Page not created")

        for selector in selectors:
            try:
                if await self.page.query_selector(selector):
                    return True
            except Exception:
                continue
        return False
    
    async def take_screenshot(self, path: str) -> None:
        """Take screenshot
        
        Args:
            path: Output file path
        """
        if not self.page:
            raise RuntimeError("Page not created")
        
        try:
            await self.page.screenshot(path=path)
            logger.info(f"Screenshot saved to {path}")
        
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            raise
    
    async def close(self) -> None:
        """Close browser"""
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            
            logger.info("Browser closed")
        
        except Exception as e:
            logger.error(f"Error closing browser: {e}")
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.launch()
        await self.create_context()
        await self.create_page()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
