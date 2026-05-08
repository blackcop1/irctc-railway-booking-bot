# 🔧 IRCTC Bot - Troubleshooting Guide

## Error: Pydantic Core & Rust Compilation Failure

### 🚨 The Error You Encountered

```
error: could not read metadata for file: 'rustup-init.exe'
pydantic-core==2.14.1 build failure
subprocess-exited-with-error
```

### ✅ SOLUTION (Already Fixed!)

The `requirements.txt` has been updated to use **Pydantic 1.10.13** which has pre-built wheels and doesn't require Rust compilation.

---

## 🆘 If You Still Get This Error

### Step 1: Delete Corrupted Virtual Environment

```bash
# Go to project directory
cd irctc-railway-booking-bot

# Delete old venv
rmdir /s /q venv

# Verify it's deleted
dir  # Should NOT show 'venv' folder
```

### Step 2: Create Fresh Virtual Environment

```bash
# Create new venv
python -m venv venv

# Activate it
venv\Scripts\activate

# Verify activation (should show (venv) prefix)
python --version
```

### Step 3: Clean Pip Cache

```bash
# Clear pip cache completely
pip cache purge

# Upgrade pip to latest
python -m pip install --upgrade pip

# Verify pip version
pip --version
```

### Step 4: Install Fresh Dependencies

```bash
# Install with --no-cache-dir to force fresh download
pip install -r requirements.txt --no-cache-dir

# This should work without Rust compilation errors
```

### Step 5: Install Playwright

```bash
# Install Playwright (may take 5-10 minutes)
playwright install

# On Windows, also install system dependencies
playwright install-deps
```

### Step 6: Verify Installation

```bash
# Test all critical imports
python -c "import playwright; print('✓ Playwright OK')"
python -c "import sqlalchemy; print('✓ SQLAlchemy OK')"
python -c "import pydantic; print('✓ Pydantic OK')"
python -c "import requests; print('✓ Requests OK')"

# All should print ✓ messages
```

---

## 🔍 Understanding the Original Error

### What Happened?

1. **Old requirements.txt** used `pydantic==2.5.0`
2. Pydantic 2.5.0 requires compilation of `pydantic-core` package
3. `pydantic-core` is written in **Rust**, needs Rust compiler
4. Windows doesn't have Rust compiler by default
5. Pip tried to download & install Rust
6. Download failed → Error occurred

### Why the Fix Works

New **`pydantic==1.10.13`** has:
- ✅ **Pre-compiled wheels** for Windows
- ✅ **No Rust dependency**
- ✅ **Same functionality** for our use case
- ✅ **Faster installation**

---

## 🛠️ Alternative Solutions (If Above Doesn't Work)

### Option 1: Install Microsoft C++ Build Tools

If you absolutely need Pydantic 2.x:

1. Download [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/downloads/)
2. Select "Desktop development with C++" workload
3. Install (~3GB, takes 20-30 minutes)
4. Restart computer
5. Try `pip install -r requirements.txt` again

### Option 2: Install Rust Toolchain

```bash
# Download Rustup from https://rustup.rs/
# Or use:
choco install rustup -y

# After Rust is installed, retry:
pip install -r requirements.txt
```

### Option 3: Use Pre-compiled Wheels

```bash
# Download pre-built pydantic wheel from:
# https://pypi.org/project/pydantic/#files

# Download: pydantic-2.5.0-cp313-cp313-win_amd64.whl (for Python 3.13)
# Or appropriate version for your Python

# Then install:
pip install C:\path\to\pydantic-2.5.0-cp313-cp313-win_amd64.whl
```

---

## 🎯 Checking Your Python Version

Different Python versions need different wheels:

```bash
# Check your Python version
python --version

# Examples:
# Python 3.8 → cp38
# Python 3.9 → cp39
# Python 3.10 → cp310
# Python 3.11 → cp311
# Python 3.12 → cp312
# Python 3.13 → cp313
```

If using Python 3.13, wheels for pydantic 2.x might not exist yet. Using Python 3.11 or 3.12 is recommended.

---

## 📋 Recommended Python Versions

| Version | Status | Recommendation |
|---------|--------|-----------------|
| 3.8 | Older | ✓ Works, but outdated |
| 3.9 | Stable | ✓ Good choice |
| 3.10 | Stable | ✓ Recommended |
| 3.11 | Latest | ✓✓ Best option |
| 3.12 | Current | ✓✓ Best option |
| 3.13 | Bleeding edge | ⚠ Use Pydantic 1.x only |

**Recommended:** Install **Python 3.11 or 3.12** from [python.org](https://www.python.org/downloads/)

---

## 🧪 Testing After Fix

### Quick Test

```bash
# Activate venv
venv\Scripts\activate

# Run simple test
python -c "
import asyncio
from src.services import IRCTCBookingService
print('✓ All imports successful!')
"
```

### Full Test

Create `test_installation.py`:
```python
"""Test installation of all dependencies"""

def test_imports():
    """Test all critical imports"""
    try:
        import playwright
        print("✓ Playwright installed")
        
        import sqlalchemy
        print("✓ SQLAlchemy installed")
        
        import pydantic
        print("✓ Pydantic installed")
        
        import requests
        print("✓ Requests installed")
        
        import ntplib
        print("✓ ntplib installed")
        
        import asyncio
        print("✓ asyncio available")
        
        print("\n✅ ALL DEPENDENCIES OK!")
        return True
    
    except ImportError as e:
        print(f"❌ Missing: {e}")
        return False

if __name__ == "__main__":
    test_imports()
```

Run test:
```bash
python test_installation.py
```

---

## 🔄 Complete Fresh Installation (Nuclear Option)

If everything fails, start completely fresh:

```bash
# 1. Delete project folder and re-clone
cd ..
rmdir /s /q irctc-railway-booking-bot
git clone https://github.com/blackcop1/irctc-railway-booking-bot.git
cd irctc-railway-booking-bot

# 2. Python version check
python --version  # Should be 3.9+

# 3. Create new venv
python -m venv venv
venv\Scripts\activate

# 4. Fresh install
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt --no-cache-dir
playwright install

# 5. Test
python -c "import playwright; print('OK')"

# Done!
```

---

## 📞 Getting Help

### Before Asking for Help, Check:

1. ✅ Python version (3.9+): `python --version`
2. ✅ Virtual env activated: `(venv)` shows in prompt
3. ✅ Latest requirements.txt used
4. ✅ Pip cache cleared: `pip cache purge`
5. ✅ Fresh venv created: `rmdir /s venv` then recreated

### When Reporting Issues, Include:

```bash
# Run this and share output:
python --version
pip --version
pip list
pip install -r requirements.txt  # Full output
```

---

## 🚀 Performance Optimization (Optional)

After successful installation:

```bash
# Precompile Python bytecode
python -m compileall src/

# This speeds up subsequent runs by ~10%
```

---

## 🎓 Understanding Package Installation

### Normal Package (Pure Python)
```
📥 Download → Install → Use
     ✅ Fast
```

### Package with C Extensions (like pydantic 2.x)
```
📥 Download source → 🔨 Compile → Install → Use
     ⚠ Needs compiler (Rust/C++)
```

### Package with Pre-built Wheels (like pydantic 1.x)
```
📥 Download wheel → Install → Use
     ✅ Fast, no compilation
```

---

## 💡 Pro Tips

### Tip 1: Always Update pip First
```bash
python -m pip install --upgrade pip
```

### Tip 2: Use --no-cache-dir for Clean Install
```bash
pip install package_name --no-cache-dir
```

### Tip 3: Check Package Size Before Install
```bash
# Large packages (>100MB) might indicate compilation needed
pip index versions package_name
```

### Tip 4: Use Python 3.10+ for Better Wheels
Newer Python versions have more pre-built wheels available.

---

## ✅ Final Checklist

Before considering your setup complete:

- [ ] Python 3.9+ installed
- [ ] Virtual environment created and activated
- [ ] requirements.txt installed without errors
- [ ] Playwright installed with `playwright install`
- [ ] All imports working (test script passes)
- [ ] `.env` file configured with credentials
- [ ] Test booking attempt successful
- [ ] Logs created in `logs/` directory

---

## 🎉 Success!

Once you see:
```
✓ Playwright OK
✓ SQLAlchemy OK
✓ Pydantic OK
✓ Requests OK
```

You're ready to book tickets! 🚂

---

**Last Updated:** May 8, 2026  
**Tested On:** Windows 10/11, Python 3.9-3.12
