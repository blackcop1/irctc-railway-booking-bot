"""Notification utilities for booking status updates."""

import os
import smtplib
from email.mime.text import MIMEText

from .logger import setup_logger

logger = setup_logger(__name__)


class NotificationManager:
    """Send optional status notifications via configured channels."""

    def __init__(self) -> None:
        self.email_enabled = (
            os.getenv("ENABLE_EMAIL_NOTIFICATIONS", "false").lower() == "true"
        )
        self.smtp_server = os.getenv("SMTP_SERVER", "")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.notification_email = os.getenv("NOTIFICATION_EMAIL", "")

    def notify_booking_status(self, success: bool, message: str) -> None:
        """Dispatch booking status notifications."""
        if self.email_enabled:
            self._send_email(
                subject=(
                    "IRCTC Booking Success"
                    if success
                    else "IRCTC Booking Failed"
                ),
                body=message,
            )

    def _send_email(self, subject: str, body: str) -> None:
        if not (
            self.smtp_server
            and self.smtp_username
            and self.smtp_password
            and self.notification_email
        ):
            logger.warning(
                "Email notification skipped due to incomplete SMTP config"
            )
            return

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = self.smtp_username
        msg["To"] = self.notification_email

        try:
            with smtplib.SMTP(
                self.smtp_server,
                self.smtp_port,
                timeout=15,
            ) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.sendmail(
                    self.smtp_username,
                    [self.notification_email],
                    msg.as_string(),
                )
            logger.info("Email notification sent")
        except Exception as exc:
            logger.error(
                f"Failed to send email notification: {exc}"
            )
