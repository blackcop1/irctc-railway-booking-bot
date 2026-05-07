# 🚂 IRCTC Railway Booking Automation Bot

A high-speed, cross-platform (Windows/Linux) automation suite for railway ticket booking with smart timing, captcha bypass, and intelligent form filling.

## 🎯 Features

### Core Capabilities
- ✅ **NTP Time Synchronization** - Millisecond-level accuracy with IRCTC servers
- ✅ **Smart Booking Logic** - Automated Tatkal (11:00 AM) and AC (10:00 AM) booking
- ✅ **Captcha Solving** - 2Captcha API integration for instant bypass
- ✅ **Browser Automation** - Playwright-based high-speed form filling
- ✅ **Master Passenger List** - Pre-configured profiles with preferences
- ✅ **Live Countdown Timer** - Shows seconds until booking window
- ✅ **Payment Automation** - IRCTC eWallet and UPI integration
- ✅ **Intelligent Retry Logic** - Exponential backoff with auto-recovery

### IRCTC-Specific Features
- 🎫 **Berth Preferences** - Logic for Lower/Side Lower/Upper berths
- 👥 **Quota Selection** - General, Ladies, Divyangjan, Senior Citizen quotas
- 🍱 **Meal Selection** - Automate Veg/Non-Veg/Jain preferences
- 🔄 **Auto-Vikalp** - Automatic alternative train seat booking
- 💳 **Travel Insurance** - Auto-toggle during checkout
- ✔️ **Aadhaar Verification** - Pre-check for Tatkal eligibility

## 📊 Performance Targets
- **Booking Success Rate**: 80%+
- **Execution Time**: <5 seconds from window opening
- **Captcha Solve Rate**: >95%
- **System Uptime**: 99.5%

## 🛠️ Technical Stack
- **Language**: Python 3.9+
- **Browser Automation**: Playwright
- **GUI**: PyQt5
- **Time Sync**: ntplib
- **Database**: SQLite + SQLAlchemy
- **Captcha API**: 2Captcha
- **HTTP Client**: httpx

## 📁 Project Structure
```
irctc-railway-booking-bot/
├── src/
│   ├── core/              # Core automation modules
│   ├── browser/           # Playwright automation
│   ├── gui/               # PyQt5 GUI components
│   ├── database/          # SQLite models
│   ├── utils/             # Config, logging, constants
│   └── main.py            # Entry point
├── tests/                 # Unit & integration tests
├── config/                # Configuration templates
├── requirements.txt       # Python dependencies
├── setup.py               # Package installer
└── LICENSE                # MIT License
```

## 🚀 Quick Start

### Windows
```bash
# Clone repository
git clone https://github.com/blackcop1/irctc-railway-booking-bot.git
cd irctc-railway-booking-bot

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python src/main.py
```

### Linux
```bash
# Clone repository
git clone https://github.com/blackcop1/irctc-railway-booking-bot.git
cd irctc-railway-booking-bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python3 src/main.py
```

## ⚙️ Configuration

1. Copy `config/config.example.yml` to `config/config.yml`
2. Add your IRCTC credentials and API keys:
   ```yaml
   IRCTC:
     username: "your_username"
     password: "your_password"
     tatkal_time: "11:00:00"
   
   CAPTCHA:
     provider: "2captcha"
     api_key: "your_api_key"
   ```

3. Configure passenger profiles in the GUI

## 📈 Booking Timeline

| Event | Time | Action |
|-------|------|--------|
| System Sync | T-90s | Initialize browser, sync NTP |
| Pre-Login | T-60s | Pre-emptive login |
| Navigate | T-45s | Go to Passenger Info page |
| Load Data | T-30s | Load pre-filled passenger data |
| Execute | T-0s | Submit form at exact timestamp |
| Payment | T+5s | Handle payment flow |

## 🔐 Security

- Encrypted credential storage
- OAuth2 support for IRCTC
- No hardcoded passwords
- Secure API key management
- HTTPS-only communication

## 📝 Logging

All activities are logged to `logs/` directory with rotation:
- Application logs: `logs/app.log`
- Booking attempts: `logs/booking.log`
- Error traces: `logs/error.log`

## 🧪 Testing

Run tests with pytest:
```bash
pytest tests/ -v
```

## 📚 Documentation

Detailed documentation for each module is available in the source files:
- [Core Modules](src/core/README.md)
- [Browser Automation](src/browser/README.md)
- [GUI Components](src/gui/README.md)
- [Database Models](src/database/README.md)

## ⚠️ Disclaimer

This tool is for educational and personal use only. Users are responsible for:
- Compliance with IRCTC Terms of Service
- Legal implications of automation in their jurisdiction
- Account suspension risks
- Ethical use of the system

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 👤 Author

**blackcop1** - Senior Software Engineer & Automation Specialist

## 🙏 Acknowledgments

- IRCTC for providing the booking platform
- Playwright team for excellent browser automation
- 2Captcha for reliable captcha solving
- Community contributors and testers

---

**Status**: 🚀 Production Ready | **Version**: 1.0.0 | **Updated**: May 2026
