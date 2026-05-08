"""IRCTC Booking Service for automated railway ticket booking."""

import asyncio
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List, Any, Callable, Awaitable
from ..utils.logger import setup_logger
from ..utils.notifications import NotificationManager
from ..utils.constants import (
    IRCTC_BASE_URL,
    TATKAL_SLEEPER_TIME,
    TATKAL_AC_TIME,
    PRE_LOGIN_OFFSET,
    PRE_FILL_OFFSET,
)
from ..core import TimeSync, CaptchaSolver, RetryHandler
from ..browser import BrowserAutomation
from ..browser.selectors import LOGIN_SELECTORS, SEARCH_SELECTORS, BOOKING_SELECTORS
from ..database import (
    DatabaseManager,
    DatabaseOperations,
    BookingAttempt,
    BookingLog,
    TrainInfo,
)

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
        self.notifier = NotificationManager()
        
        # Session state
        self.is_logged_in = False
        self.booking_session = None

    async def _execute_with_retries(
        self,
        label: str,
        operation: Callable[[], Awaitable[Any]],
    ) -> Any:
        """Run async operation with retry/backoff."""
        attempt = 0
        delay = self.retry_handler.initial_delay
        last_error: Optional[Exception] = None

        while attempt < self.retry_handler.max_attempts:
            try:
                return await operation()
            except Exception as exc:
                attempt += 1
                last_error = exc
                if attempt >= self.retry_handler.max_attempts:
                    break
                logger.warning(
                    f"{label} failed at attempt {attempt}/{self.retry_handler.max_attempts}: {exc}"
                )
                await asyncio.sleep(delay)
                delay = min(
                    delay * self.retry_handler.backoff_multiplier,
                    self.retry_handler.max_delay,
                )

        raise RuntimeError(
            f"{label} failed after {self.retry_handler.max_attempts} attempts"
        ) from last_error

    def _create_booking_attempt(
        self,
        train_number: str,
        passengers: List[Dict[str, str]],
        from_station: str,
        to_station: str,
        travel_date: str,
        class_type: str,
        quota: str,
    ) -> BookingAttempt:
        db_session = self.db_manager.get_session()
        db_ops = DatabaseOperations(db_session)
        try:
            attempt = BookingAttempt(
                user_id=1,
                from_station=from_station,
                to_station=to_station,
                travel_date=datetime.strptime(travel_date, "%d-%m-%Y"),
                train_number=train_number,
                class_type=class_type,
                quota=quota,
                num_passengers=len(passengers),
                status="pending",
                attempted_at=datetime.now(),
                booking_confirmation=json.dumps(
                    {"passengers": passengers}, ensure_ascii=False
                ),
            )
            db_ops.add(attempt)
            return attempt
        finally:
            db_ops.close()

    def _update_attempt(
        self,
        attempt_id: int,
        status: str,
        pnr: Optional[str] = None,
        error_message: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        db_session = self.db_manager.get_session()
        db_ops = DatabaseOperations(db_session)
        try:
            attempt = db_ops.query(BookingAttempt).filter_by(id=attempt_id).first()
            if not attempt:
                return

            attempt.status = status
            attempt.pnr = pnr
            attempt.error_message = error_message
            attempt.completed_at = datetime.now()
            if details is not None:
                attempt.booking_confirmation = json.dumps(details, ensure_ascii=False)
            db_ops.update(attempt)
        finally:
            db_ops.close()

    def _log_attempt_event(
        self,
        attempt_id: int,
        action: str,
        status: str,
        details: str = "",
    ) -> None:
        db_session = self.db_manager.get_session()
        db_ops = DatabaseOperations(db_session)
        try:
            db_ops.add(
                BookingLog(
                    booking_attempt_id=attempt_id,
                    action=action,
                    status=status,
                    details=details,
                )
            )
        finally:
            db_ops.close()

    async def _capture_debug_artifacts(self, prefix: str) -> Dict[str, str]:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        debug_dir = Path("logs/debug")
        debug_dir.mkdir(parents=True, exist_ok=True)
        screenshot_path = debug_dir / f"{prefix}_{timestamp}.png"
        html_path = debug_dir / f"{prefix}_{timestamp}.html"

        artifacts: Dict[str, str] = {}
        try:
            await self.browser.take_screenshot(str(screenshot_path))
            artifacts["screenshot"] = str(screenshot_path)
        except Exception:
            pass

        if self.browser.page:
            try:
                html_path.write_text(
                    await self.browser.page.content(),
                    encoding="utf-8",
                )
                artifacts["html"] = str(html_path)
            except Exception:
                pass

        return artifacts

    async def _ensure_logged_in(self) -> bool:
        if self.is_logged_in and self.browser.page:
            current_url = self.browser.page.url.lower()
            if "/login" not in current_url:
                return True
        return await self.login()

    async def _extract_train_rows(self) -> List[Dict[str, Any]]:
        if not self.browser.page:
            return []

        data = await self.browser.page.evaluate(
            """
            () => {
              const rows = [];
              const cards = document.querySelectorAll(
                "app-train-list .train_avl_enq_box, .train_avl_enq_box, table tbody tr"
              );
              cards.forEach((card) => {
                const text = card.innerText || "";
                const numberMatch = text.match(/\\b\\d{5}\\b/);
                const trainNumber = numberMatch ? numberMatch[0] : "";
                const lines = text.split("\\n").map(v => v.trim()).filter(Boolean);
                const trainName = lines.find(v => /EXP|SF|MAIL|RAJDHANI|SHATABDI|DURONTO|INTERCITY/i.test(v)) || (lines[1] || "");
                const departure = (text.match(/\\b([01]?\\d|2[0-3]):[0-5]\\d\\b/g) || [])[0] || "";
                const arrival = (text.match(/\\b([01]?\\d|2[0-3]):[0-5]\\d\\b/g) || [])[1] || "";
                if (trainNumber) {
                  rows.push({
                    train_number: trainNumber,
                    train_name: trainName || "Unknown",
                    departure_time: departure,
                    arrival_time: arrival,
                    raw: text
                  });
                }
              });
              return rows;
            }
            """
        )
        return data if isinstance(data, list) else []

    def _upsert_train_cache(
        self, trains: List[Dict[str, Any]], from_station: str, to_station: str
    ) -> None:
        db_session = self.db_manager.get_session()
        db_ops = DatabaseOperations(db_session)
        try:
            for train in trains:
                number = train.get("train_number")
                if not number:
                    continue
                train_row = db_ops.query(TrainInfo).filter_by(train_number=number).first()
                if train_row:
                    train_row.train_name = train.get("train_name", train_row.train_name)
                    train_row.from_station = from_station
                    train_row.to_station = to_station
                    train_row.departure_time = train.get("departure_time", "")
                    train_row.arrival_time = train.get("arrival_time", "")
                    db_ops.update(train_row)
                else:
                    db_ops.add(
                        TrainInfo(
                            train_number=number,
                            train_name=train.get("train_name", "Unknown"),
                            from_station=from_station,
                            to_station=to_station,
                            departure_time=train.get("departure_time", ""),
                            arrival_time=train.get("arrival_time", ""),
                        )
                    )
        finally:
            db_ops.close()

    async def _extract_pnr(self) -> Optional[str]:
        if not self.browser.page:
            return None
        body_text = await self.browser.page.inner_text("body")
        match = re.search(r"\bPNR\s*[:\-]?\s*(\d{10})\b", body_text, re.IGNORECASE)
        if match:
            return match.group(1)
        return None
    
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

            async def _login_once() -> bool:
                await self.browser.goto(f"{IRCTC_BASE_URL}/nget/booking/login")
                await self.browser.fill_any(LOGIN_SELECTORS["username"], self.username)
                await self.browser.fill_any(LOGIN_SELECTORS["password"], self.password)

                if self.browser.page:
                    captcha_node = await self.browser.page.query_selector(
                        LOGIN_SELECTORS["captcha_image"][0]
                    )
                    if captcha_node:
                        captcha_src = await captcha_node.get_attribute("src")
                        captcha_solution = self.captcha_solver.solve_image_captcha(
                            captcha_src or ""
                        )
                        if not captcha_solution:
                            raise RuntimeError("Failed to solve captcha")
                        await self.browser.fill_any(
                            LOGIN_SELECTORS["captcha_input"], captcha_solution
                        )

                await self.browser.click_any(LOGIN_SELECTORS["submit"])
                await self.browser.page.wait_for_load_state("networkidle")
                current_url = self.browser.page.url.lower()
                return "/login" not in current_url

            result = await self._execute_with_retries("login", _login_once)
            self.is_logged_in = bool(result)
            if self.is_logged_in:
                logger.info("Successfully logged in to IRCTC")
            return self.is_logged_in
        except Exception as e:
            self.is_logged_in = False
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
            
            if not await self._ensure_logged_in():
                logger.error("Cannot search trains without active session")
                return []

            await self.browser.goto(f"{IRCTC_BASE_URL}/nget/booking/train-search")
            await self.browser.fill_any(SEARCH_SELECTORS["from_station"], from_station)
            await self.browser.fill_any(SEARCH_SELECTORS["to_station"], to_station)
            await self.browser.fill_any(SEARCH_SELECTORS["travel_date"], travel_date)

            for class_selector in SEARCH_SELECTORS["class_select"]:
                if self.browser.page:
                    class_select = await self.browser.page.query_selector(class_selector)
                    if class_select:
                        try:
                            await self.browser.page.select_option(
                                class_selector, class_type
                            )
                            break
                        except Exception:
                            continue

            await self.browser.click_any(SEARCH_SELECTORS["search_button"])
            await self.browser.page.wait_for_load_state("networkidle")
            await self.browser.wait_for_any(SEARCH_SELECTORS["result_rows"], timeout_ms=45000)

            trains = await self._extract_train_rows()
            self._upsert_train_cache(trains, from_station, to_station)

            logger.info(f"Train search completed with {len(trains)} trains")
            return trains
        
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
        attempt = self._create_booking_attempt(
            train_number=train_number,
            passengers=passengers,
            from_station=from_station,
            to_station=to_station,
            travel_date=travel_date,
            class_type=class_type,
            quota=quota,
        )
        self._log_attempt_event(attempt.id, "booking_started", "pending", train_number)

        try:
            logger.info(f"Booking train {train_number} for {len(passengers)} passengers")

            if not await self._ensure_logged_in():
                raise RuntimeError("Session expired and re-login failed")

            clicked = await self.browser.page.evaluate(
                """
                (trainNumber) => {
                  const allRows = Array.from(
                    document.querySelectorAll(
                      "app-train-list .train_avl_enq_box, .train_avl_enq_box, table tbody tr"
                    )
                  );
                  for (const row of allRows) {
                    const text = row.innerText || "";
                    if (text.includes(trainNumber)) {
                      const btn = row.querySelector("button");
                      if (btn) {
                        btn.click();
                        return true;
                      }
                    }
                  }
                  return false;
                }
                """,
                train_number,
            )
            if not clicked:
                await self.browser.click_any(SEARCH_SELECTORS["book_button"])
            await self.browser.page.wait_for_load_state("networkidle")
            self._log_attempt_event(attempt.id, "train_selected", "success", train_number)

            if self.browser.page:
                name_inputs = await self.browser.page.query_selector_all(
                    BOOKING_SELECTORS["passenger_name_inputs"][0]
                )
                age_inputs = await self.browser.page.query_selector_all(
                    BOOKING_SELECTORS["passenger_age_inputs"][0]
                )
                gender_selects = await self.browser.page.query_selector_all(
                    BOOKING_SELECTORS["passenger_gender_selects"][0]
                )
                berth_selects = await self.browser.page.query_selector_all(
                    BOOKING_SELECTORS["berth_selects"][0]
                )

                for index, passenger in enumerate(passengers):
                    if index < len(name_inputs):
                        await name_inputs[index].fill(str(passenger.get("name", "")))
                    if index < len(age_inputs):
                        await age_inputs[index].fill(str(passenger.get("age", "")))
                    if index < len(gender_selects):
                        await gender_selects[index].select_option(
                            str(passenger.get("gender", "M"))
                        )
                    if index < len(berth_selects) and passenger.get("berth_preference"):
                        await berth_selects[index].select_option(
                            str(passenger["berth_preference"])
                        )

            await self.browser.click_any(BOOKING_SELECTORS["continue_button"])
            await self.browser.page.wait_for_load_state("networkidle")
            self._log_attempt_event(attempt.id, "passenger_details", "success")

            pnr = await self._extract_pnr()
            if pnr:
                self._update_attempt(
                    attempt.id,
                    status="success",
                    pnr=pnr,
                    details={"train_number": train_number, "pnr": pnr},
                )
                self._log_attempt_event(attempt.id, "booking_completed", "success", pnr)
                self.notifier.notify_booking_status(
                    success=True,
                    message=f"Booking successful for {train_number}. PNR: {pnr}",
                )
                return pnr

            if await self.browser.exists_any(BOOKING_SELECTORS["payment_page_marker"]):
                self._update_attempt(
                    attempt.id,
                    status="pending_payment",
                    details={
                        "train_number": train_number,
                        "message": "Reached payment boundary; manual payment required",
                    },
                )
                self._log_attempt_event(
                    attempt.id,
                    "payment_boundary_reached",
                    "pending",
                    "Manual payment required",
                )
                self.notifier.notify_booking_status(
                    success=True,
                    message=(
                        f"Reached payment page for {train_number}. "
                        "Complete payment manually."
                    ),
                )
                return None

            raise RuntimeError("Booking submitted but no PNR/payment state detected")

        except Exception as e:
            artifacts = await self._capture_debug_artifacts("booking_error")
            error_text = f"{e}. Artifacts: {artifacts}" if artifacts else str(e)
            self._update_attempt(
                attempt.id,
                status="failed",
                error_message=error_text,
                details={"train_number": train_number, "error": str(e)},
            )
            self._log_attempt_event(attempt.id, "booking_failed", "failed", error_text)
            self.notifier.notify_booking_status(
                success=False,
                message=f"Booking failed for {train_number}: {e}",
            )
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
        
        tatkal_time = TATKAL_SLEEPER_TIME if class_type.upper() == "SL" else TATKAL_AC_TIME
        now = self.time_sync.get_synced_time()
        target_datetime = datetime.combine(now.date(), tatkal_time)
        if now >= target_datetime:
            target_datetime += timedelta(days=1)

        pre_login_time = target_datetime - timedelta(seconds=PRE_LOGIN_OFFSET)
        pre_fill_time = target_datetime - timedelta(seconds=PRE_FILL_OFFSET)
        logger.info(
            f"Tatkal schedule prepared: pre-login={pre_login_time}, "
            f"pre-fill={pre_fill_time}, submit={target_datetime}"
        )
        self.time_sync.wait_until(pre_login_time)
        await self._ensure_logged_in()
        self.time_sync.wait_until(pre_fill_time)

        logger.info(f"Waiting for Tatkal window: {tatkal_time}")
        self.time_sync.wait_until(target_datetime)
        logger.info("Tatkal window opened!")

    def get_booking_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Fetch recent booking attempt history."""
        db_session = self.db_manager.get_session()
        db_ops = DatabaseOperations(db_session)
        try:
            rows = (
                db_ops.query(BookingAttempt)
                .order_by(BookingAttempt.attempted_at.desc())
                .limit(limit)
                .all()
            )
            return [
                {
                    "id": row.id,
                    "train_number": row.train_number,
                    "from_station": row.from_station,
                    "to_station": row.to_station,
                    "status": row.status,
                    "pnr": row.pnr,
                    "attempted_at": row.attempted_at.isoformat()
                    if row.attempted_at
                    else None,
                }
                for row in rows
            ]
        finally:
            db_ops.close()

    def get_booking_stats(self) -> Dict[str, int]:
        """Fetch high-level booking counters."""
        db_session = self.db_manager.get_session()
        db_ops = DatabaseOperations(db_session)
        try:
            total = db_ops.query(BookingAttempt).count()
            success = db_ops.query(BookingAttempt).filter_by(status="success").count()
            failed = db_ops.query(BookingAttempt).filter_by(status="failed").count()
            return {"total": total, "success": success, "failed": failed}
        finally:
            db_ops.close()
    
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
