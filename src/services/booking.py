"""IRCTC Booking Service for automated railway ticket booking"""

import asyncio
from datetime import datetime, time
from typing import Optional, Dict, List, Any
from ..utils.logger import setup_logger
from ..utils.constants import (
    IRCTC_BASE_URL,
    BOOKING_TIMEOUT,
    TATKAL_SLEEPER_TIME,
    TATKAL_AC_TIME,
)
from ..core import TimeSync, CaptchaSolver, RetryHandler
from ..browser import BrowserAutomation
from ..database import DatabaseManager, DatabaseOperations, BookingAttempt, TrainInfo

logger = setup_logger(__name__)


class IRCTCBookingService:
    """Main IRCTC booking service"""

    def __init__(
        self,
        username: str,
        password: str,
        captcha_api_key: str,
        headless: bool = False,
        use_ntp_sync: bool = True,
    ):
        """Initialize IRCTC booking service
        
        Args:
            username: IRCTC username
            password: IRCTC password
            captcha_api_key: 2Captcha API key
            headless: Run browser in headless mode
            use_ntp_sync: Enable NTP time synchronization
        """
        self.username = username
        self.password = password
        self.captcha_api_key = captcha_api_key
        self.headless = headless
        self.use_ntp_sync = use_ntp_sync
        
        # Initialize components
        self.browser = BrowserAutomation(headless=headless)
        self.time_sync = TimeSync() if use_ntp_sync else None
        self.captcha_solver = CaptchaSolver(captcha_api_key)
        self.retry_handler = RetryHandler()
        self.db_manager = DatabaseManager()
        
        # Session state
        self.is_logged_in = False
        self.booking_session = None
    
    async def initialize(self) -> None:
        """Initialize service components"""
        try:
            logger.info("Initializing IRCTC booking service...")
            
            # Initialize database
            self.db_manager.initialize()
            
            # Sync time if enabled
            if self.use_ntp_sync:
                if not self.time_sync.sync():
                    logger.warning("NTP synchronization failed. Using system time.")
            
            # Launch browser
            await self.browser.launch()
            await self.browser.create_context()
            await self.browser.create_page()
            
            logger.info("IRCTC booking service initialized successfully")
        
        except Exception as e:
            logger.error(f"Failed to initialize service: {e}")
            raise
    
    async def login(self) -> bool:
        """Login to IRCTC website
        
        Returns:
            True if login successful, False otherwise
        """
        try:
            logger.info("Attempting to login to IRCTC...")
            
            # Navigate to login page
            await self.browser.goto(f"{IRCTC_BASE_URL}/nget/booking/login")
            
            # Fill username
            await self.browser.fill_input("input[name='userid']", self.username)
            logger.debug("Username filled")
            
            # Fill password
            await self.browser.fill_input("input[name='password']", self.password)
            logger.debug("Password filled")
            
            # Solve captcha
            captcha_image = await self.browser.page.query_selector("img[alt='captcha']")
            if captcha_image:
                captcha_src = await captcha_image.get_attribute("src")
                captcha_solution = self.captcha_solver.solve_image_captcha(captcha_src)
                
                if not captcha_solution:
                    logger.error("Failed to solve captcha")
                    return False
                
                # Fill captcha
                await self.browser.fill_input("input[name='captcha']", captcha_solution)
                logger.debug("Captcha filled")
            
            # Submit login form
            await self.browser.click("button[type='submit']")
            
            # Wait for redirect
            await self.browser.page.wait_for_load_state("networkidle")
            
            # Check if login successful
            current_url = self.browser.page.url
            if "dashboard" in current_url or "booking" in current_url:
                self.is_logged_in = True
                logger.info("Successfully logged in to IRCTC")
                return True
            else:
                logger.error("Login failed - redirect unsuccessful")
                return False
        
        except Exception as e:
            logger.error(f"Login error: {e}")
            return False
    
    async def search_trains(
        self,
        from_station: str,
        to_station: str,
        travel_date: str,
        passenger_count: int = 1,
        class_type: str = "SL",
    ) -> List[Dict[str, Any]]:
        """Search for trains
        
        Args:
            from_station: Departure station code
            to_station: Destination station code
            travel_date: Travel date (DD-MM-YYYY)
            passenger_count: Number of passengers
            class_type: Class type code
        
        Returns:
            List of available trains
        """
        try:
            logger.info(f"Searching trains: {from_station} → {to_station} on {travel_date}")
            
            # Navigate to booking page
            await self.browser.goto(f"{IRCTC_BASE_URL}/nget/booking/train-search")
            
            # Fill search criteria
            await self.browser.fill_input("input[name='fromStationCode']", from_station)
            await self.browser.fill_input("input[name='toStationCode']", to_station)
            await self.browser.fill_input("input[name='travelDate']", travel_date)
            
            # Select class
            await self.browser.click(f"select[name='class'] option[value='{class_type}']")
            
            # Submit search
            await self.browser.click("button[name='search']")
            
            # Wait for results
            await self.browser.page.wait_for_load_state("networkidle")
            
            logger.info("Train search completed")
            return []
        
        except Exception as e:
            logger.error(f"Train search error: {e}")
            return []
    
    async def book_train(
        self,
        train_number: str,
        passengers: List[Dict[str, str]],
        from_station: str,
        to_station: str,
        travel_date: str,
        class_type: str = "SL",
        quota: str = "GN",
    ) -> Optional[str]:
        """Book train tickets
        
        Args:
            train_number: Train number to book
            passengers: List of passenger details
            from_station: Departure station
            to_station: Destination station
            travel_date: Travel date (DD-MM-YYYY)
            class_type: Class type
            quota: Quota type
        
        Returns:
            PNR number if booking successful, None otherwise
        """
        try:
            logger.info(f"Booking train {train_number} for {len(passengers)} passengers")
            
            # Record booking attempt
            db_session = self.db_manager.get_session()
            db_ops = DatabaseOperations(db_session)
            
            booking_attempt = BookingAttempt(
                user_id=1,  # TODO: Get from session
                from_station=from_station,
                to_station=to_station,
                travel_date=datetime.strptime(travel_date, "%d-%m-%Y"),
                train_number=train_number,
                class_type=class_type,
                quota=quota,
                num_passengers=len(passengers),
                status="pending",
            )
            db_ops.add(booking_attempt)
            
            # Proceed with booking
            # TODO: Implement actual booking logic
            
            logger.info(f"Booking process completed for {train_number}")
            return None
        
        except Exception as e:
            logger.error(f"Booking error: {e}")
            return None
    
    async def wait_for_tatkal_window(self, class_type: str = "SL") -> None:
        """Wait until Tatkal booking window opens
        
        Args:
            class_type: Class type (SL for Sleeper, AC for AC classes)
        """
        if not self.time_sync:
            logger.warning("NTP sync not enabled. Tatkal timing may be inaccurate.")
            return
        
        tatkal_time = TATKAL_SLEEPER_TIME if class_type == "SL" else TATKAL_AC_TIME
        today = datetime.now().date()
        target_datetime = datetime.combine(today, tatkal_time)
        
        logger.info(f"Waiting for Tatkal window: {tatkal_time}")
        self.time_sync.wait_until(target_datetime)
        logger.info("Tatkal window opened!")
    
    async def close(self) -> None:
        """Close service and cleanup resources"""
        try:
            await self.browser.close()
            self.db_manager.close()
            logger.info("IRCTC booking service closed")
        
        except Exception as e:
            logger.error(f"Error closing service: {e}")
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
