# 🚀 ONE-CLICK LAUNCHER

**The easiest way to run the Sports Medicine application!**

---

## ⚡ Quick Start (Just 2 Steps!)

### Step 1: Install Prerequisites (One Time Only)

Before the first run, make sure you have:

**Python 3.9+**
- Download: https://python.org/downloads/
- ✅ **IMPORTANT:** Check "Add Python to PATH" during installation
- Restart computer after installing

**Node.js (LTS)**
- Download: https://nodejs.org/
- Install with default settings
- Restart computer after installing

### Step 2: Run the App

**Double-click:** `RUN_APP.bat`

That's it! The script will automatically:
- ✅ Check if Python and Node.js are installed
- ✅ Create virtual environment (if needed)
- ✅ Install all backend dependencies (if needed)
- ✅ Install all frontend dependencies (if needed)
- ✅ Start the backend server
- ✅ Start the frontend server
- ✅ Open your browser to the application

---

## ⏱️ How Long Does It Take?

**First Run (with installation):**
- Backend dependencies: ~2-3 minutes
- Frontend dependencies: ~3-5 minutes
- **Total: 5-8 minutes**

**Subsequent Runs:**
- Dependencies already installed
- Just starts the servers
- **Total: ~15-20 seconds**

---

## 📺 What You'll See

When you run `RUN_APP.bat`:

```
========================================
Sports Medicine - ONE CLICK LAUNCHER
========================================

[1/7] Checking Python installation...
Python 3.11.0
Python is installed!

[2/7] Checking Node.js installation...
v18.17.0
Node.js is installed!

[3/7] Setting up Python virtual environment...
Virtual environment already exists.

[4/7] Checking backend dependencies...
Backend dependencies already installed.

[5/7] Checking frontend dependencies...
Frontend dependencies already installed.

[6/7] Starting Backend Server...
Backend server starting...

[7/7] Starting Frontend Server...
Frontend server starting...

========================================
SUCCESS! Application Started!
========================================

Opening browser now...
```

Then:
- 🟢 Two terminal windows open (Backend & Frontend)
- 🌐 Browser opens to http://127.0.0.1:3000
- 🎉 You're ready to use the app!

---

## ✅ First Run Checklist

On the very first run, you'll see:

```
[3/7] Setting up Python virtual environment...
Creating virtual environment...
Virtual environment created!

[4/7] Checking backend dependencies...
Backend dependencies not found. Installing...
This will take 2-3 minutes...
Installing backend packages...
✓ Successfully installed fastapi uvicorn sqlalchemy pandas...

[5/7] Checking frontend dependencies...
Frontend dependencies not found. Installing...
This will take 3-5 minutes...
✓ Frontend dependencies installed successfully!
```

This only happens once! After that, it just starts the app.

---

## 🛑 How to Stop the Application

**Option 1: Close Windows**
- Close the "Backend" terminal window
- Close the "Frontend" terminal window

**Option 2: Use Stop Script**
- Double-click `STOP_APP.bat`

**Option 3: Ctrl+C**
- In each terminal window, press `Ctrl+C`

---

## 🔴 Error Messages & Solutions

### "Python is NOT installed!"
**What it means:** Python isn't installed or not in PATH

**Fix:**
1. Download Python from https://python.org
2. During installation, CHECK "Add Python to PATH"
3. Restart your computer
4. Run `RUN_APP.bat` again

---

### "Node.js is NOT installed!"
**What it means:** Node.js isn't installed or not in PATH

**Fix:**
1. Download Node.js from https://nodejs.org
2. Install with default settings
3. Restart your computer
4. Run `RUN_APP.bat` again

---

### "Failed to install backend dependencies"
**What it means:** pip couldn't download packages

**Fix:**
1. Check internet connection
2. Right-click `RUN_APP.bat` → "Run as administrator"
3. Temporarily disable antivirus
4. Try again

---

### "Failed to install frontend dependencies"
**What it means:** npm couldn't download packages

**Fix:**
1. Check internet connection
2. Delete `frontend\node_modules` folder
3. Run `RUN_APP.bat` again

---

### Two terminal windows open but browser doesn't
**What it means:** Servers started but browser didn't auto-open

**Fix:**
- Manually open browser
- Go to: http://127.0.0.1:3000

---

### "Address already in use" or "Port 8000/3000 in use"
**What it means:** Servers are already running

**Fix:**
1. Run `STOP_APP.bat`
2. Wait 5 seconds
3. Run `RUN_APP.bat` again

---

## 💡 Pro Tips

### Create Desktop Shortcut
1. Right-click `RUN_APP.bat`
2. Choose "Send to" → "Desktop (create shortcut)"
3. Rename to "Sports Medicine App"
4. Double-click the desktop icon to launch!

### Pin to Taskbar
1. Create a shortcut (see above)
2. Right-click the shortcut
3. Choose "Pin to taskbar"
4. Click the taskbar icon to launch!

### Run on Startup
1. Press `Windows + R`
2. Type: `shell:startup`
3. Copy `RUN_APP.bat` to the folder that opens
4. App will launch automatically when Windows starts

---

## 🆚 Other Launcher Files vs RUN_APP.bat

| File | What It Does | When to Use |
|------|--------------|-------------|
| **RUN_APP.bat** | Everything automatically | **Use this!** Best for everyone |
| SETUP.bat | Only installs dependencies | If you want to install first, then run later |
| START_APP.bat | Starts app (validates dependencies) | If dependencies are installed |
| QUICK_START.bat | Starts app (no validation) | Advanced users only |
| FIX_BACKEND.bat | Reinstalls backend only | If backend dependencies are broken |
| FIX_FRONTEND.bat | Reinstalls frontend only | If frontend dependencies are broken |

**Recommendation:** Just use `RUN_APP.bat` for everything!

---

## 📱 What You Get

After the browser opens, you'll see:

**Navigation:**
- 🏠 Team Dashboard (view all athletes & risk levels)
- 👥 Manage Athletes (add/edit/delete athletes)
- 📤 Upload Data (CSV files for training, treatments, injuries)
- 🔌 Connection Test (diagnostic page)

**Features:**
- Color-coded risk indicators (🟢 Low, 🟡 Medium, 🔴 High)
- Interactive charts (ACWR trends, training loads)
- Risk calculations with personalized recommendations
- CSV upload with auto-parsing
- Individual athlete detailed analytics

---

## 🔄 Daily Usage

**Every day, just:**
1. Double-click `RUN_APP.bat`
2. Wait 15-20 seconds
3. Browser opens automatically
4. Start using the app!

**When done:**
1. Close both terminal windows
2. Or run `STOP_APP.bat`

---

## ✨ Summary

**One file does everything:**
```
📁 sports_medicine/
   └── RUN_APP.bat  👈 DOUBLE-CLICK THIS!
```

**First time:**
- Takes 5-8 minutes (installs everything)

**Every time after:**
- Takes 15-20 seconds (just starts servers)

**No more:**
- ❌ Running multiple scripts
- ❌ Typing commands
- ❌ Figuring out what to do
- ❌ Manual installation steps

**Just:**
- ✅ Double-click
- ✅ Wait
- ✅ Use the app!

---

Happy coaching! 🏃‍♂️💪
