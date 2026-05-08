"""Constants for IRCTC Railway Booking Bot"""

from datetime import time

# IRCTC URLs
IRCTC_BASE_URL = "https://www.irctc.co.in"
IRCTC_API_URL = "https://api.irctc.co.in"

# Booking Window Times
TATKAL_SLEEPER_TIME = time(11, 0, 0)  # 11:00 AM
TATKAL_AC_TIME = time(10, 0, 0)       # 10:00 AM

# Timeouts (in seconds)
BOOKING_TIMEOUT = 300  # 5 minutes
DEFAULT_PAGE_TIMEOUT = 60  # 60 seconds (INCREASED FROM 30)
PAYMENT_TIMEOUT = 180  # 3 minutes

# NTP Servers
NTP_SERVERS = [
    "pool.ntp.org",
    "time.nist.gov",
    "time.google.com",
    "time.cloudflare.com",
]

# Retry Configuration
MAX_RETRIES = 5
INITIAL_RETRY_DELAY = 1  # seconds
MAX_RETRY_DELAY = 30  # seconds
BACKOFF_MULTIPLIER = 2

# Captcha Configuration
CAPTCHA_TIMEOUT = 300  # 5 minutes
CAPTCHA_MAX_RETRIES = 3

# Browser Configuration
DEFAULT_VIEWPORT_WIDTH = 1920
DEFAULT_VIEWPORT_HEIGHT = 1080

# Database Configuration
DATABASE_PATH = "data/booking.db"
LOG_DIR = "logs"

# Quota Types
QUOTA_GENERAL = "General"
QUOTA_LADIES = "Ladies"
QUOTA_DIVYANGJAN = "Divyangjan"
QUOTA_SENIOR_CITIZEN = "Senior Citizen"

QUOTA_OPTIONS = [
    QUOTA_GENERAL,
    QUOTA_LADIES,
    QUOTA_DIVYANGJAN,
    QUOTA_SENIOR_CITIZEN,
]

# Berth Preferences
BERTH_LOWER = "Lower"
BERTH_SIDE_LOWER = "Side Lower"
BERTH_UPPER = "Upper"
BERTH_MIDDLE = "Middle"

BERTH_OPTIONS = [
    BERTH_LOWER,
    BERTH_SIDE_LOWER,
    BERTH_UPPER,
    BERTH_MIDDLE,
]

# Food Preferences
FOOD_VEG = "Veg"
FOOD_NON_VEG = "Non-Veg"
FOOD_JAIN = "Jain"

FOOD_OPTIONS = [
    FOOD_VEG,
    FOOD_NON_VEG,
    FOOD_JAIN,
]

# Class Types
CLASS_SLEEPER = "Sleeper"
CLASS_AC_FIRST = "AC First"
CLASS_AC_2_TIER = "AC 2-Tier"
CLASS_AC_3_TIER = "AC 3-Tier"
CLASS_FIRST = "First"
CLASS_GENERAL = "General"

CLASS_OPTIONS = [
    CLASS_SLEEPER,
    CLASS_AC_FIRST,
    CLASS_AC_2_TIER,
    CLASS_AC_3_TIER,
    CLASS_FIRST,
    CLASS_GENERAL,
]

# User Agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Pre-booking Offsets (in seconds)
PRE_LOGIN_OFFSET = 60  # 60 seconds before window
PRE_FILL_OFFSET = 45   # 45 seconds before window
FORM_SUBMIT_OFFSET = 0  # At exact window time

# System Limits
MAX_PASSENGERS_PER_BOOKING = 6
MIN_PASSENGERS_PER_BOOKING = 1
MAX_PASSENGER_AGE = 120
MIN_PASSENGER_AGE = 0
