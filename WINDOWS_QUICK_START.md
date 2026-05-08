# 🚀 Windows Quick Start Guide - IRCTC Railway Booking Bot

## ⚡ 5-Minute Setup (For the Impatient)

### Step 1: Install Python (2 minutes)
```bash
# Download from https://www.python.org/downloads/
# ✓ CHECK: "Add Python to PATH"
# ✓ CLICK: "Install Now"
```

### Step 2: Clone & Setup (2 minutes)
```bash
# Open Command Prompt (Win + R, type: cmd)
git clone https://github.com/blackcop1/irctc-railway-booking-bot.git
cd irctc-railway-booking-bot

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate
```

### Step 3: Install Dependencies (1 minute)
```bash
# IMPORTANT: Update pip first
python -m pip install --upgrade pip

# Install requirements (uses pre-built wheels, no Rust needed!)
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

✅ **Done!** Now configure `.env` file and run it.

---

## 🔧 Fixing the Pydantic/Rust Error

### Problem
You got this error:
```
error: could not read metadata for file: 'rustup-init.exe'
pydantic-core build failure
```

### Solution ✓ (Already Fixed!)

The `requirements.txt` has been updated to use:
- ✅ `pydantic==1.10.13` (instead of 2.5.0) - has pre-built wheels
- ✅ No Rust compiler needed
- ✅ Works on all Windows versions

**To fix your current installation:**

```bash
# 1. Delete old virtual environment
rmdir /s venv

# 2. Create new one
python -m venv venv

# 3. Activate
venv\Scripts\activate

# 4. Upgrade pip
python -m pip install --upgrade pip

# 5. Install fresh dependencies
pip install -r requirements.txt

# 6. Install Playwright
playwright install
```

---

## 📋 Complete Installation Checklist

### ✓ Prerequisites
- [ ] Windows 10/11 (64-bit)
- [ ] Internet connection (min 2 Mbps)
- [ ] 2GB free disk space

### ✓ Installation Steps
- [ ] Python installed (3.8+) with PATH configured
- [ ] Git installed (optional, can download as ZIP)
- [ ] Repository cloned/extracted
- [ ] Virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Playwright browsers installed (`playwright install`)

### ✓ Configuration
- [ ] `.env` file created (copy from `.env.example`)
- [ ] IRCTC credentials added
- [ ] 2Captcha API key added
- [ ] Booking details configured

### ✓ Testing
- [ ] Run: `python -c "import playwright; print('OK')"`
- [ ] Run: `python main.py --help`
- [ ] Run test booking

---

## 🎯 Quick Configuration

### Create `.env` file:
```bash
# Copy the template
copy .env.example .env

# Edit with Notepad
notepad .env
```

### Minimal `.env` content:
```env
IRCTC_USERNAME=your_irctc_username
IRCTC_PASSWORD=your_irctc_password
CAPTCHA_API_KEY=your_2captcha_api_key
FROM_STATION=NDLS
TO_STATION=MMCT
TRAVEL_DATE=15-05-2026
CLASS_TYPE=SL
QUOTA=GN
HEADLESS=false
```

---

## ▶️ Running Your First Booking

### Option 1: Command Line (Easiest)
```bash
# Make sure venv is activated
venv\Scripts\activate

# Run booking
python main.py
```

### Option 2: With Custom Parameters
```bash
python main.py ^
  --from NDLS ^
  --to MMCT ^
  --date 15-05-2026 ^
  --class SL ^
  --quota GN
```

### Option 3: Using Config File
```bash
# Create config.json
python main.py --config config.json
```

---

## 📊 Expected Output

When everything works:
```
Starting IRCTC Railway Booking Bot
Booking route: NDLS → MMCT
Travel date: 15-05-2026, Class: SL, Quota: GN
Step 1: Logging in to IRCTC...
✓ Successfully logged in
Step 2: Searching for trains...
✓ Found 15 trains
Step 3: Booking train 12345 (Rajdhani Express)...
✓ Booking successful! PNR: 1234567890
```

---

## ⚠️ Common Issues & Quick Fixes

### Issue 1: `'python' is not recognized`
```bash
# Solution: Reinstall Python and CHECK "Add to PATH"
# Or use: python -m pip ... (instead of pip)
python -m pip install -r requirements.txt
```

### Issue 2: `ModuleNotFoundError: No module named 'playwright'`
```bash
# Solution: Activate virtual environment first
venv\Scripts\activate

# Then install
pip install -r requirements.txt
```

### Issue 3: Playwright Install Fails
```bash
# Solution: Install system dependencies
playwright install-deps

# If still fails, download directly
playwright install chromium --with-deps
```

### Issue 4: `Permission denied` errors
```bash
# Solution: Run Command Prompt as Administrator
# Right-click cmd → Run as administrator
# Then run pip install commands
```

### Issue 5: CAPTCHA Solving Fails
```bash
# Solution: Check 2Captcha balance
# Visit: https://2captcha.com/user/account

# Add balance (minimum ₹100 or $2)
# Wait 1-2 minutes for activation
```

---

## 🧪 Testing Your Setup

Create `test_setup.py`:
```python
import asyncio
from src.services import IRCTCBookingService

async def test_connection():
    try:
        service = IRCTCBookingService(
            username="test",
            password="test",
            captcha_api_key="test"
        )
        await service.initialize()
        print("✓ Browser OK")
        await service.close()
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_connection())
    exit(0 if result else 1)
```

Run it:
```bash
python test_setup.py
```

---

## 📱 Scheduling Automated Bookings

### Windows Task Scheduler Method

**Create `schedule_booking.bat`:**
```batch
@echo off
cd D:\MY SUMMER PROJECTS\irctc-railway-booking-bot
call venv\Scripts\activate.bat
python main.py
```

**Schedule it:**
1. Press `Win + R`
2. Type: `taskschd.msc`
3. Click "Create Basic Task"
4. Name: "IRCTC Tatkal Booking"
5. Trigger: "Daily" at 10:30 AM
6. Action: "Start a program" → Select your `.bat` file
7. Click "OK"

**Test it works:**
```bash
# Run manually to test
taskschd.msc  # right-click task → Run
```

---

## 🔐 Keeping Credentials Safe

### ✓ Good Practice:
```env
# .env file (NOT committed to Git)
IRCTC_PASSWORD=YourPassword123
CAPTCHA_API_KEY=abc123def456
```

### ✗ Bad Practice:
- ❌ Sharing `.env` file
- ❌ Hardcoding passwords in code
- ❌ Committing `.env` to GitHub

### Secure Setup:
```bash
# Add to .gitignore (already done)
echo .env >> .gitignore

# Never commit:
git add .
git commit -m "Setup" --
# (Won't include .env)
```

---

## 🚀 Advanced: Running 24/7

### Option 1: Windows Service (Advanced)
```bash
# Install as service (requires admin)
pip install pywin32
pyinstaller --onefile main.py
# Create Windows service (complex, requires coding)
```

### Option 2: Scheduled Task (Recommended)
- Use Windows Task Scheduler (see above)
- Run daily at Tatkal time

### Option 3: Always-On PC
- Keep PC on
- Setup automatic login
- Create scheduled task
- PC auto-runs booking at specified time

---

## 💡 Pro Tips

### Tip 1: Multiple Bookings
```bash
# Create separate .env files
copy .env .env.route1
copy .env .env.route2

# Use in scripts
python main.py --config config.route1.json
```

### Tip 2: Error Debugging
```bash
# Run with verbose logging
set LOG_LEVEL=DEBUG
python main.py
```

### Tip 3: Fast Retry Setup
```env
MAX_RETRIES=10
INITIAL_RETRY_DELAY=1
AUTO_RETRY_ON_FAILURE=true
```

### Tip 4: Check Logs
```bash
# View recent logs
type logs\irctc_bot.log | tail -50

# Or use PowerShell
Get-Content logs\irctc_bot.log -Tail 50
```

---

## 📞 Getting Help

### Check Logs
```bash
# Open logs directory
explorer logs\

# View latest log
notepad logs\irctc_bot.log
```

### Verify Each Component
```bash
# Test Python
python --version

# Test pip
pip --version

# Test Playwright
python -c "import playwright; print('OK')"

# Test SQLAlchemy
python -c "import sqlalchemy; print('OK')"

# Test requests
python -c "import requests; print('OK')"
```

### Common Error Messages

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError` | Activate venv: `venv\Scripts\activate` |
| `playwright install` fails | Run as admin, use `--with-deps` |
| Captcha timeout | Check 2Captcha balance |
| Connection refused | Check internet, try different network |
| Invalid credentials | Verify password manually on IRCTC website |
| Port 9222 in use | Kill other Playwright processes |

---

## 🎯 Quick Command Reference

```bash
# Activate virtual environment
venv\Scripts\activate

# Deactivate virtual environment
deactivate

# Install/update dependencies
pip install -r requirements.txt -U

# Run bot
python main.py

# Run with parameters
python main.py --from NDLS --to MMCT --date 15-05-2026

# View logs
type logs\irctc_bot.log

# List installed packages
pip list

# Clean up
pip cache purge
```

---

## ✅ Verification Checklist Before Booking

- [ ] Python installed and in PATH
- [ ] Virtual environment activated (shows `(venv)` in prompt)
- [ ] All dependencies installed (`pip list` shows all packages)
- [ ] `.env` file configured with credentials
- [ ] 2Captcha API key is valid and has balance
- [ ] IRCTC credentials tested manually on website
- [ ] System time is accurate (check clock)
- [ ] Internet connection is stable
- [ ] Playwright browsers installed (`playwright install` ran successfully)

---

## 🎉 You're Ready!

```bash
# Final test
(venv) D:\path> python main.py --help

# If you see the help menu, you're good to go!
# Now configure .env and book your tickets!
```

---

**Last Updated:** May 8, 2026  
**For Issues:** Check SETUP_AND_USAGE_GUIDE.md  
**Documentation:** See README.md
