# 🚀 EASY INSTALL GUIDE - Windows 11

Got the **"No module named 'uvicorn'"** error? Follow these steps:

---

## 📋 What You Need First

Before anything else, install these (if not already installed):

### 1. **Python** (Required)
- Go to: **https://python.org/downloads/**
- Download Python 3.9 or newer
- **CRITICAL**: During installation, CHECK the box "Add Python to PATH"
- Click "Install Now"
- Restart your computer after installation

### 2. **Node.js** (Required)
- Go to: **https://nodejs.org/**
- Download the LTS version
- Install with default settings
- Restart your computer after installation

---

## ✅ STEP-BY-STEP FIX

### Step 1: Verify Python and Node.js

Open **Command Prompt** and type:
```
python --version
```
Should show: `Python 3.x.x`

Then type:
```
node --version
```
Should show: `v18.x.x` or similar

**If either command gives an error:**
- You need to install that software (see above)
- Or Python/Node.js is not in your PATH (reinstall and check "Add to PATH")

---

### Step 2: Navigate to Your Project

Open **Command Prompt** and go to your project folder:
```
cd C:\Users\YourName\Downloads\sports_medicine-main
```
(Replace with your actual path)

---

### Step 3: Install Backend Dependencies

**Double-click:** `FIX_BACKEND.bat`

OR run manually:
```
cd C:\Users\YourName\Downloads\sports_medicine-main
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Wait 2-3 minutes** for installation to complete.

You should see:
```
Successfully installed fastapi uvicorn sqlalchemy pandas...
```

---

### Step 4: Install Frontend Dependencies

**Double-click:** `FIX_FRONTEND.bat`

OR run manually:
```
cd C:\Users\YourName\Downloads\sports_medicine-main\frontend
npm install
```

**Wait 3-5 minutes** for installation to complete.

---

### Step 5: Start the Application

**Double-click:** `START_APP.bat`

You should see:
- Two terminal windows open (Backend and Frontend)
- Browser opens to http://127.0.0.1:3000
- No more "module not found" errors!

---

## 🔴 Common Errors & Fixes

### "Python is not recognized"
**Problem:** Python not installed or not in PATH

**Fix:**
1. Uninstall Python
2. Download fresh from python.org
3. During install, **CHECK "Add Python to PATH"**
4. Restart computer
5. Run `python --version` to verify

---

### "npm is not recognized"
**Problem:** Node.js not installed or not in PATH

**Fix:**
1. Download and install Node.js from nodejs.org
2. Restart computer
3. Run `node --version` to verify

---

### "Access is denied" or "Permission denied"
**Problem:** Windows security blocking installation

**Fix:**
1. Right-click FIX_BACKEND.bat
2. Choose "Run as administrator"
3. Same for FIX_FRONTEND.bat

---

### "No module named 'uvicorn'" (Even After Install)
**Problem:** Virtual environment not activated

**Fix:**
```
cd C:\path\to\sports_medicine
venv\Scripts\activate
```
You should see `(venv)` at the start of your prompt.

Then try running again.

---

### Dependencies Install But App Still Won't Start
**Problem:** Old/corrupted installation

**Fix - Complete Clean Reinstall:**
1. Delete these folders:
   - `venv`
   - `frontend\node_modules`
2. Run `FIX_BACKEND.bat`
3. Run `FIX_FRONTEND.bat`
4. Run `START_APP.bat`

---

## 📝 Installation Checklist

Use this to make sure everything is done:

- [ ] Python 3.9+ installed
- [ ] "Add Python to PATH" was checked during install
- [ ] Node.js LTS installed
- [ ] Computer restarted after installations
- [ ] `python --version` works in Command Prompt
- [ ] `node --version` works in Command Prompt
- [ ] Ran `FIX_BACKEND.bat` successfully
- [ ] Ran `FIX_FRONTEND.bat` successfully
- [ ] `venv` folder exists
- [ ] `frontend\node_modules` folder exists
- [ ] Can run `START_APP.bat` without errors

---

## 🎯 Quick Command Reference

**Check if Python installed:**
```
python --version
```

**Check if Node.js installed:**
```
node --version
```

**Install backend dependencies:**
```
cd C:\path\to\sports_medicine
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Install frontend dependencies:**
```
cd C:\path\to\sports_medicine\frontend
npm install
```

**Start backend manually:**
```
cd C:\path\to\sports_medicine
venv\Scripts\activate
python run_backend.py
```

**Start frontend manually (new window):**
```
cd C:\path\to\sports_medicine\frontend
npm run dev
```

---

## 🆘 Still Having Issues?

1. **Take a screenshot** of the error
2. **Note what step** you're on
3. **Check** that Python and Node.js are installed
4. **Try** running as Administrator
5. **Check** antivirus isn't blocking

---

## ✨ Success Looks Like This:

**Backend Terminal:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
Initializing database...
Database initialized successfully!
```

**Frontend Terminal:**
```
VITE v5.x.x  ready in xxx ms
➜  Local:   http://127.0.0.1:3000/
```

**Browser:**
- Opens to http://127.0.0.1:3000
- Shows "Sports Medicine - Injury Prevention System"
- No network errors!

---

Good luck! 🍀
