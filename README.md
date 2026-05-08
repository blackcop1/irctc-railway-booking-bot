# 🚂 IRCTC Railway Booking Bot

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)](https://github.com/blackcop1/irctc-railway-booking-bot)
[![Status](https://img.shields.io/badge/status-Active-brightgreen)]()

**Automated Indian Railways (IRCTC) Ticket Booking Bot**

[Features](#-features) • [Quick Start](#-quick-start) • [Installation](#-installation) • [Usage](#-usage-guide) • [Documentation](#-documentation)

</div>

---

## 🎯 Features

### 🤖 Automation
- ✅ **Fully Automated Booking** - No manual intervention needed
- ✅ **Tatkal Support** - Book at exact 11:00 AM / 10:00 AM
- ✅ **NTP Time Sync** - Precise timing using Network Time Protocol
- ✅ **Auto Captcha Solving** - 2Captcha integration for automatic CAPTCHA resolution
- ✅ **Multi-Quota Support** - General, Tatkal, Premium Tatkal, Railway Staff

### 🔐 Security & Reliability
- ✅ **Secure Credentials** - Environment-based configuration, never hardcoded
- ✅ **Retry Mechanism** - Exponential backoff for failed attempts
- ✅ **Error Handling** - Comprehensive exception handling and logging
- ✅ **Browser Automation** - Playwright for reliable browser control

### 💾 Database & Tracking
- ✅ **Booking History** - Track all booking attempts in SQLite database
- ✅ **User Management** - Store multiple user profiles
- ✅ **Analytics** - View booking statistics and success rates
- ✅ **PNR Tracking** - Save and retrieve PNR information

### 📊 Flexibility
- ✅ **CLI Interface** - Command-line arguments for easy automation
- ✅ **Configuration Files** - JSON/YAML config support
- ✅ **Environment Variables** - All settings configurable via .env
- ✅ **Scheduled Tasks** - Windows Task Scheduler / Cron integration
- ✅ **Multiple Routes** - Book different routes with separate configs

### 📝 Logging & Monitoring
- ✅ **Detailed Logs** - JSON formatted structured logging
- ✅ **Debug Mode** - Verbose output for troubleshooting
- ✅ **Performance Metrics** - Track booking response times
- ✅ **Email Notifications** - Get booking status via email

---

## ⚡ Quick Start (2 Minutes)

### Prerequisites
- **Python 3.8+** installed with PATH configured
- **2GB** free disk space
- **Internet connection** (2+ Mbps)

### Installation
```bash
# Clone repository
git clone https://github.com/blackcop1/irctc-railway-booking-bot.git
cd irctc-railway-booking-bot

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # Linux/macOS

# Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
playwright install

# Configure
copy .env.example .env
notepad .env  # Edit with your credentials
```

### Run
```bash
python main.py
```

**[📖 Full Setup Guide →](WINDOWS_QUICK_START.md)**

---

## 📦 Installation

### Step 1: Python Installation

**Windows:**
1. Download from [python.org](https://www.python.org/downloads/)
2. ✅ Check "Add Python to PATH"
3. Click "Install Now"
4. Verify: `python --version`

**Linux/macOS:**
```bash
# macOS (using Homebrew)
brew install python3

# Ubuntu/Debian
sudo apt-get install python3 python3-pip python3-venv
```

### Step 2: Clone Repository
```bash
git clone https://github.com/blackcop1/irctc-railway-booking-bot.git
cd irctc-railway-booking-bot
```

### Step 3: Virtual Environment
```bash
# Create
python -m venv venv

# Activate
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS
```

### Step 4: Dependencies
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install all packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install

# (Windows only) Install system dependencies
playwright install-deps
```

### Step 5: Configuration
```bash
# Copy template
copy .env.example .env  # Windows
cp .env.example .env  # Linux/macOS

# Edit with your credentials
notepad .env  # Windows
nano .env  # Linux/macOS
```

**[🔧 Detailed Installation Guide →](SETUP_AND_USAGE_GUIDE.md)**

---

## ⚙️ Configuration

### Create `.env` File

```env
# IRCTC Credentials
IRCTC_USERNAME=your_irctc_username
IRCTC_PASSWORD=your_irctc_password

# Captcha API (get from https://2captcha.com)
CAPTCHA_API_KEY=your_2captcha_api_key

# Booking Details
FROM_STATION=NDLS        # New Delhi
TO_STATION=MMCT          # Mumbai Central
TRAVEL_DATE=15-05-2026   # DD-MM-YYYY format

# Preferences
CLASS_TYPE=SL            # SL, AC2, AC3, 1A, 2A, 3A, GN
QUOTA=TQ                 # GN (General), TQ (Tatkal), PT (Premium)

# Settings
HEADLESS=false           # false = see browser, true = background
LOG_LEVEL=INFO           # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### Station Codes Reference

| Code | Station | Code | Station |
|------|---------|------|---------|
| NDLS | New Delhi | MMCT | Mumbai Central |
| HWH | Howrah | CSMT | Mumbai CST |
| KOAA | Kolkata | MAS | Chennai Central |
| SC | Secunderabad | KYJ | Kanpur |
| BRC | Vadodara | JP | Jaipur |

[📍 Full Station List →](SETUP_AND_USAGE_GUIDE.md#station-code-reference)

---

## 🎮 Usage Guide

### Method 1: Command Line (Recommended)

```bash
# Basic booking with .env file
python main.py

# With custom parameters
python main.py \
  --username your_username \
  --password your_password \
  --captcha-key your_api_key \
  --from NDLS \
  --to MMCT \
  --date 15-05-2026 \
  --class SL \
  --quota TQ
```

### Method 2: Configuration File

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
  "quota": "TQ",
  "headless": false
}
```

Run:
```bash
python main.py --config config.json
```

### Method 3: Python Script

```python
import asyncio
from main import main

async def book_ticket():
    success = await main(
        username="your_username",
        password="your_password",
        captcha_api_key="your_api_key",
        from_station="NDLS",
        to_station="MMCT",
        travel_date="15-05-2026",
        class_type="SL",
        quota="TQ"
    )
    return success

if __name__ == "__main__":
    result = asyncio.run(book_ticket())
    print("✓ Success!" if result else "✗ Failed!")
```

### Method 4: Windows Task Scheduler

Create `run_booking.bat`:
```batch
@echo off
cd D:\path\to\project
call venv\Scripts\activate.bat
python main.py
pause
```

Schedule:
1. Press `Win + R`
2. Type: `taskschd.msc`
3. Create Task → Set trigger to "Daily 10:30 AM"
4. Set action to run your `.bat` file

**[🎯 Complete Usage Guide →](SETUP_AND_USAGE_GUIDE.md#usage-guide)**

---

## 🛠️ Troubleshooting

### Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError` | Virtual env not activated | Run `venv\Scripts\activate` |
| Pydantic/Rust error | Old requirements.txt | Use updated `requirements.txt` |
| Playwright not found | Not installed | Run `playwright install` |
| CAPTCHA timeout | Insufficient balance | Add balance to 2Captcha account |
| Login failed | Wrong credentials | Verify manually on IRCTC website |
| Connection timeout | Network issue | Check internet, try different network |

### Debug Mode

Enable detailed logging:
```bash
# Set log level
set LOG_LEVEL=DEBUG
python main.py

# Or in .env
LOG_LEVEL=DEBUG
```

View logs:
```bash
type logs\irctc_bot.log  # Windows
cat logs/irctc_bot.log   # Linux/macOS
tail -f logs/irctc_bot.log  # Live view
```

**[🔍 Full Troubleshooting Guide →](SETUP_AND_USAGE_GUIDE.md#troubleshooting)**

---

## 📖 Documentation

- **[Windows Quick Start](WINDOWS_QUICK_START.md)** - Fast setup for Windows users
- **[Complete Setup Guide](SETUP_AND_USAGE_GUIDE.md)** - Detailed instructions with examples
- **[API Reference](SETUP_AND_USAGE_GUIDE.md#api-reference)** - Code examples and API docs
- **[Troubleshooting](SETUP_AND_USAGE_GUIDE.md#troubleshooting)** - Solutions for common issues

---

## 🏗️ Project Structure

```
irctc-railway-booking-bot/
├── src/
│   ├── core/                 # Core functionality
│   │   ├── time.py          # NTP time synchronization
│   │   ├── captcha.py       # Captcha solving
│   │   ├── retry.py         # Retry mechanism
│   │   └── __init__.py
│   ├── browser/              # Browser automation
│   │   ├── automation.py    # Playwright wrapper
│   │   └── __init__.py
│   ├── database/             # Database layer
│   │   ├── models.py        # SQLAlchemy ORM models
│   │   ├── manager.py       # Database operations
│   │   └── __init__.py
│   ├── services/             # Business logic
│   │   ├── booking.py       # Main booking service
│   │   └── __init__.py
│   └── utils/                # Utilities
│       ├── logger.py        # Logging setup
│       ├── constants.py     # Configuration constants
│       └── __init__.py
├── main.py                   # Application entry point
├── requirements.txt          # Python dependencies
├── .env.example             # Configuration template
├── WINDOWS_QUICK_START.md   # Windows setup guide
├── SETUP_AND_USAGE_GUIDE.md # Detailed documentation
└── README.md                # This file
```

---

## 🔧 Technologies Used

- **[Playwright](https://playwright.dev/)** - Browser automation
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - Database ORM
- **[2Captcha API](https://2captcha.com/)** - Captcha solving
- **[ntplib](https://pypi.org/project/ntplib/)** - Time synchronization
- **[Python asyncio](https://docs.python.org/3/library/asyncio.html)** - Async operations

---

## ⚠️ Important Disclaimers

### Legal Notice
- This bot **violates IRCTC Terms of Service** - use at your own risk
- IRCTC may ban automated access attempts
- The author is **not responsible** for account bans or legal consequences
- Use for **personal use only**

### Ethical Guidelines
- ✅ Do use responsibly and sparingly
- ✅ Do respect server resources
- ✅ Do keep credentials private
- ❌ Don't sell or redistribute
- ❌ Don't use for commercial purposes
- ❌ Don't spam the IRCTC servers

### Data Privacy
- Your credentials are stored **locally in .env**
- Never commit `.env` to Git
- 2Captcha will see images but processes them securely
- Booking data is stored in local SQLite database

---

## 📊 Performance Metrics

| Metric | Typical Value |
|--------|---------------|
| Login Time | 5-10 seconds |
| Train Search | 3-5 seconds |
| Captcha Solving | 10-30 seconds |
| Booking Submission | 2-5 seconds |
| **Total Time** | **30-60 seconds** |

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙋 Support & Help

### Getting Help
1. Check [Troubleshooting Guide](SETUP_AND_USAGE_GUIDE.md#troubleshooting)
2. Review logs in `logs/irctc_bot.log`
3. Enable DEBUG mode for detailed output
4. Check existing [GitHub Issues](https://github.com/blackcop1/irctc-railway-booking-bot/issues)

### Report Issues
- Create [GitHub Issue](https://github.com/blackcop1/irctc-railway-booking-bot/issues) with:
  - Error message and logs
  - Steps to reproduce
  - Your OS and Python version

---

## 🎓 Learning Resources

- **Python Async:** [Real Python - Async IO](https://realpython.com/async-io-python/)
- **Playwright:** [Official Documentation](https://playwright.dev/python/)
- **SQLAlchemy:** [ORM Tutorial](https://docs.sqlalchemy.org/en/20/orm/)
- **IRCTC API:** [Unofficial Documentation](https://github.com/search?q=irctc+api)

---

## 🚀 What's Next?

### Planned Features
- [ ] Web UI Dashboard
- [ ] Email notifications on booking
- [ ] Telegram bot integration
- [ ] Multiple simultaneous bookings
- [ ] Waitlist auto-cancellation
- [ ] Refund status tracking
- [ ] Machine learning for seat prediction

### Version History
- **v1.0.0** (May 2026) - Initial release with basic booking automation

---

## 💬 Feedback

Have suggestions? Found a bug? Let me know!
- 🐛 [Report Bug](https://github.com/blackcop1/irctc-railway-booking-bot/issues)
- 💡 [Request Feature](https://github.com/blackcop1/irctc-railway-booking-bot/issues)
- ⭐ [Star the repo](https://github.com/blackcop1/irctc-railway-booking-bot)

---

<div align="center">

**Made with ❤️ by [Tushar Sudarshee](https://github.com/blackcop1)**

[⬆ Back to Top](#-irctc-railway-booking-bot)

</div>
