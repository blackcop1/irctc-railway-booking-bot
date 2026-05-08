# IRCTC Railway Booking Bot - Complete Setup & Usage Guide

## 📋 Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation Guide](#installation-guide)
3. [Configuration](#configuration)
4. [Usage Guide](#usage-guide)
5. [Troubleshooting](#troubleshooting)
6. [API Reference](#api-reference)

---

## System Requirements

### Hardware Requirements
- **Processor:** Intel i5/AMD Ryzen 5 or better
- **RAM:** 4GB minimum (8GB recommended)
- **Storage:** 2GB free space
- **Internet:** Stable broadband connection (min 2 Mbps)

### Software Requirements
- **OS:** Windows 10/11 (64-bit)
- **Python:** 3.8 or higher
- **Browser:** Chrome/Chromium (will be installed by Playwright)

---

## Installation Guide

### Step 1: Install Python

1. Visit [python.org](https://www.python.org/downloads/)
2. Download Python 3.11 (or latest 3.x version)
3. **Important:** During installation, CHECK the box "Add Python to PATH"
4. Click "Install Now"

**Verify Installation:**
```bash
python --version
pip --version
```

### Step 2: Clone the Repository

```bash
# Open Command Prompt (Win + R, type cmd)
git clone https://github.com/blackcop1/irctc-railway-booking-bot.git
cd irctc-railway-booking-bot
```

**Note:** If Git is not installed:
1. Download from [git-scm.com](https://git-scm.com/download/win)
2. Install with default options
3. Restart Command Prompt

### Step 3: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

**Your prompt should now show:** `(venv) C:\path\to\project>`

### Step 4: Install Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install

# Install Playwright system dependencies
playwright install-deps
```

⏳ **This will take 5-10 minutes** (Playwright downloads Chrome automatically)

### Step 5: Verify Installation

```bash
python -c "import playwright; print('✓ Playwright OK')"
python -c "import sqlalchemy; print('✓ SQLAlchemy OK')"
python -c "import requests; print('✓ Requests OK')"
```

---

## Configuration

### Step 1: Create .env File

1. Copy `.env.example` to `.env`:
```bash
copy .env.example .env
```

2. Open `.env` in Notepad (right-click → Edit)

### Step 2: Configure IRCTC Credentials

```env
# Your IRCTC login credentials
IRCTC_USERNAME=your_irctc_username
IRCTC_PASSWORD=your_irctc_password
```

### Step 3: Get 2Captcha API Key

1. Visit [2captcha.com](https://2captcha.com/)
2. Sign up for a free account
3. Add balance (₹100+ minimum for testing)
4. Go to "Settings" → Copy your API Key
5. Add to `.env`:

```env
CAPTCHA_API_KEY=your_2captcha_api_key_here
```

### Step 4: Configure Booking Details

```env
# Departure and Destination
FROM_STATION=NDLS       # Station codes (see Station Code List below)
TO_STATION=MMCT         # Mumbai Central
TRAVEL_DATE=15-05-2026  # DD-MM-YYYY format

# Booking Preferences
CLASS_TYPE=SL          # SL (Sleeper), AC2, AC3, 1A, 2A, 3A, GN
QUOTA=TQ               # GN (General), TQ (Tatkal), PT (Premium), RL (Railway Staff)
```

### Step 5: Browser Settings

```env
# Run without GUI (faster, for server deployments)
HEADLESS=false         # Set to 'true' for headless mode

# For testing/development
HEADLESS=false         # Set to 'false' to see browser window
```

### Step 6: Notification Settings (Optional)

```env
# Email Notifications
ENABLE_EMAIL_NOTIFICATIONS=true
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
NOTIFICATION_EMAIL=recipient@gmail.com
```

**For Gmail:**
1. Enable 2-Factor Authentication
2. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Generate App Password for "Mail" on "Windows PC"
4. Use this password in `.env`

### Station Code Reference

Common Station Codes:
```
NDLS    - New Delhi
MMCT    - Mumbai Central
BRC     - Vadodara
DLS     - Delhi Sarai Rohilla
CSMT    - Mumbai CST
MAO     - Mangalore
KYJ     - Kanpur
BSB     - Varanasi
HWH     - Howrah
KOAA    - Kolkata
MAS     - Chennai Central
BZA     - Vijayawada
SC      - Secunderabad
HYB     - Hyderabad
JP      - Jaipur
UDZ     - Udaipur
AGC     - Agra
GWL     - Gwalior
```

**Find more codes:** Visit IRCTC website and search trains to see station codes

---

## Usage Guide

### Method 1: Command Line Interface (CLI)

#### Basic Usage

```bash
# Simple booking with all parameters
python main.py ^
  --username your_username ^
  --password your_password ^
  --captcha-key your_api_key ^
  --from NDLS ^
  --to MMCT ^
  --date 15-05-2026 ^
  --class SL ^
  --quota GN
```

#### Using Configuration File

```bash
python main.py --config config.json
```

Create `config.json`:
```json
{
  "username": "your_username",
  "password": "your_password",
  "captcha_api_key": "your_api_key",
  "from_station": "NDLS",
  "to_station": "MMCT",
  "travel_date": "15-05-2026",
  "class_type": "SL",
  "quota": "GN",
  "headless": false
}
```

#### Using Environment Variables

```bash
# Set environment variables
set IRCTC_USERNAME=your_username
set IRCTC_PASSWORD=your_password
set CAPTCHA_API_KEY=your_api_key
set FROM_STATION=NDLS
set TO_STATION=MMCT
set TRAVEL_DATE=15-05-2026

# Run with .env file
python main.py
```

### Method 2: Python Script

Create `book_ticket.py`:

```python
import asyncio
from main import main, load_config

async def book_tatkal_ticket():
    """Book a Tatkal ticket"""
    
    config = {
        "username": "your_username",
        "password": "your_password",
        "captcha_api_key": "your_api_key",
        "from_station": "NDLS",
        "to_station": "MMCT",
        "travel_date": "15-05-2026",
        "class_type": "AC2",
        "quota": "TQ",  # Tatkal
        "headless": False,
    }
    
    success = await main(**config)
    
    if success:
        print("✓ Booking successful!")
    else:
        print("✗ Booking failed!")

if __name__ == "__main__":
    asyncio.run(book_tatkal_ticket())
```

Run it:
```bash
python book_ticket.py
```

### Method 3: Scheduled Booking (Windows Task Scheduler)

**For automated daily booking attempts:**

1. Create `schedule_booking.bat`:
```batch
@echo off
cd C:\path\to\irctc-railway-booking-bot
call venv\Scripts\activate.bat
python main.py
pause
```

2. Open Task Scheduler:
   - Win + R → `taskschd.msc`
   - Click "Create Basic Task"
   - Name: "IRCTC Booking"
   - Trigger: Daily at 11:00 AM
   - Action: Start a program → Select `schedule_booking.bat`

---

## Step-by-Step Booking Process

### For General Quota Booking

```bash
# 1. Activate virtual environment
venv\Scripts\activate

# 2. Run the bot
python main.py --from NDLS --to MMCT --date 15-05-2026 --quota GN

# Expected Output:
# ✓ Successfully logged in
# ✓ Found 15 trains
# ✓ Booking train 12345 (Rajdhani Express)
# ✓ Booking successful! PNR: 1234567890
```

### For Tatkal Booking (11 AM Slot)

```bash
# Run 30 minutes before 11 AM
# Bot will wait for exact 11:00 AM, then auto-submit

python main.py ^
  --from NDLS ^
  --to MMCT ^
  --date 15-05-2026 ^
  --class AC2 ^
  --quota TQ
```

**What happens:**
1. Bot logs in at 10:30 AM
2. Fills in booking details
3. Waits for 11:00 AM
4. Auto-submits form instantly at 11:00 AM
5. Solves captcha automatically
6. Confirms booking

---

## Troubleshooting

### Issue 1: "ModuleNotFoundError"

**Error:** `ModuleNotFoundError: No module named 'playwright'`

**Solution:**
```bash
# Reactivate virtual environment
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt -U

# Install Playwright again
playwright install
```

### Issue 2: "Captcha Solving Failed"

**Error:** `CAPTCHA_SOLVING_FAILED` or timeout

**Solution:**
1. Check 2Captcha balance: Visit [2captcha.com](https://2captcha.com/)
2. Ensure API key is correct in `.env`
3. Try increasing timeout in `.env`:
```env
CAPTCHA_TIMEOUT=300  # 5 minutes
```

### Issue 3: "Browser Not Found"

**Error:** `PlaywrightError: Browser is not installed`

**Solution:**
```bash
# Reinstall browsers
playwright install chromium

# Install system dependencies
playwright install-deps
```

### Issue 4: "Invalid Credentials"

**Error:** `LOGIN_FAILED` or "Invalid username or password"

**Solution:**
1. Verify IRCTC credentials manually at [irctc.co.in](https://www.irctc.co.in/)
2. Check `.env` file for typos
3. If password has special characters, wrap in quotes:
```env
IRCTC_PASSWORD="Pass@word#123"
```

### Issue 5: "Connection Timeout"

**Error:** `Timeout error` or "Connection refused"

**Solution:**
1. Check internet connection
2. Increase timeout in `.env`:
```env
BOOKING_TIMEOUT=600  # 10 minutes
DEFAULT_PAGE_TIMEOUT=60  # 60 seconds
```
3. Try from a different network

### Issue 6: "Port Already in Use"

**Error:** `Port 9222 is already in use`

**Solution:**
```bash
# Kill process using the port
netstat -ano | findstr :9222
taskkill /PID <PID_NUMBER> /F
```

### Enable Debug Mode

For detailed logs, create `debug.py`:

```python
import os
import asyncio
from main import main

# Enable debug logging
os.environ['LOG_LEVEL'] = 'DEBUG'

async def debug_booking():
    await main(
        username="your_username",
        password="your_password",
        captcha_api_key="your_api_key",
        from_station="NDLS",
        to_station="MMCT",
        travel_date="15-05-2026",
    )

if __name__ == "__main__":
    asyncio.run(debug_booking())
```

---

## API Reference

### IRCTCBookingService

```python
from src.services import IRCTCBookingService

# Initialize service
service = IRCTCBookingService(
    username="your_username",
    password="your_password",
    captcha_api_key="your_api_key",
    headless=False,
    use_ntp_sync=True
)

# Initialize (launch browser, sync time)
await service.initialize()

# Login
success = await service.login()

# Search trains
trains = await service.search_trains(
    from_station="NDLS",
    to_station="MMCT",
    travel_date="15-05-2026",
    passenger_count=1,
    class_type="SL"
)

# Wait for Tatkal window (11 AM for Sleeper)
await service.wait_for_tatkal_window(class_type="SL")

# Book train
pnr = await service.book_train(
    train_number="12345",
    passengers=[{
        "name": "John Doe",
        "age": "30",
        "gender": "M",
        "berth_preference": "LB"
    }],
    from_station="NDLS",
    to_station="MMCT",
    travel_date="15-05-2026",
    class_type="SL",
    quota="GN"
)

# Cleanup
await service.close()
```

### Database Operations

```python
from src.database import DatabaseManager, DatabaseOperations, User

# Initialize database
db_manager = DatabaseManager()
db_manager.initialize()

# Get session
session = db_manager.get_session()
db_ops = DatabaseOperations(session)

# Add user
user = User(username="test", email="test@example.com")
db_ops.add(user)

# Query users
users = db_ops.query(User).filter_by(username="test").all()

# Update user
user.email = "new_email@example.com"
db_ops.update(user)

# Close session
db_ops.close()
```

---

## Important Notes

⚠️ **DISCLAIMER:**
- Use this bot responsibly and ethically
- IRCTC may block automated access (violates ToS)
- Use at your own risk
- Don't sell or redistribute this code
- Respect server resources

⏱️ **Timing Tips:**
- Run bot 30 minutes before booking window
- Ensure system time is accurate (sync with NTP)
- Use stable internet connection
- Avoid multiple simultaneous bookings

💾 **Data Management:**
- All bookings are saved in `data/booking.db`
- Logs are saved in `logs/` directory
- Keep backups of `.env` file securely

---

## Getting Help

If you encounter issues:

1. Check logs: `logs/irctc_bot.log`
2. Read troubleshooting section above
3. Run in debug mode for detailed output
4. Check GitHub issues
5. Contact project maintainer

---

## Example: Complete Workflow

```bash
# 1. Activate environment
venv\Scripts\activate

# 2. Run booking 30 min before Tatkal
python main.py ^
  --username myusername ^
  --password mypassword ^
  --captcha-key my_api_key ^
  --from NDLS ^
  --to MMCT ^
  --date 15-05-2026 ^
  --class AC2 ^
  --quota TQ

# 3. Wait for success message
# ✓ Booking successful! PNR: 1234567890

# 4. Check confirmation email
# 5. Download e-ticket from IRCTC

# Done! 🎉
```

---

**Last Updated:** May 2026
**Version:** 1.0.0
**License:** MIT
