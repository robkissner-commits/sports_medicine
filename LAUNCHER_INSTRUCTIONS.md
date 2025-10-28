# Windows Launcher Scripts - Easy Start Guide

I've created several batch files to make launching the application super easy on Windows!

## 📁 Launcher Files Created

### 🟢 **START_APP.bat** (Recommended)
**What it does:**
- Checks if setup is complete, runs setup if needed
- Starts the backend server
- Starts the frontend server
- Opens your browser automatically
- Shows helpful status messages

**How to use:**
1. Double-click `START_APP.bat`
2. Wait for two terminal windows to open
3. Browser will open automatically to http://localhost:3000
4. Keep both terminal windows open while using the app

---

### 🔵 **SETUP.bat** (First Time Only)
**What it does:**
- Creates Python virtual environment
- Installs all Python dependencies
- Installs all Node.js dependencies

**When to use:**
- The very first time you download the project
- If you get "module not found" errors
- If you want to reinstall everything from scratch

**How to use:**
1. Double-click `SETUP.bat`
2. Wait 3-5 minutes for installation
3. When complete, you can use START_APP.bat

---

### ⚡ **QUICK_START.bat** (Advanced)
**What it does:**
- Starts both servers immediately
- Opens browser automatically
- No status messages or checks

**When to use:**
- After initial setup is complete
- When you want the fastest launch
- You know everything is already installed

**How to use:**
1. Double-click `QUICK_START.bat`
2. Browser opens automatically
3. That's it!

---

### 🔴 **STOP_APP.bat**
**What it does:**
- Stops both backend and frontend servers
- Closes all related terminal windows

**When to use:**
- When you're done using the application
- If servers get stuck and won't close
- Quick way to shut everything down

**How to use:**
1. Double-click `STOP_APP.bat`
2. All servers stop immediately

---

## 📋 Quick Start Instructions

### First Time Setup
```
1. Download all files from GitHub
2. Extract to a folder (e.g., C:\Users\YourName\sports_medicine)
3. Double-click SETUP.bat
4. Wait for installation (3-5 minutes)
5. Double-click START_APP.bat
6. Application opens in your browser!
```

### Daily Use
```
1. Double-click START_APP.bat
2. Use the application
3. When done, close both terminal windows
   OR double-click STOP_APP.bat
```

---

## 🎯 Recommended Workflow

**First time:**
1. Run `SETUP.bat` once
2. Run `START_APP.bat`

**Every time after:**
1. Just run `START_APP.bat` or `QUICK_START.bat`

---

## 🔧 Troubleshooting

### "Python is not recognized"
- Make sure Python is installed
- During Python installation, check "Add Python to PATH"
- Restart your computer after installing Python

### "npm is not recognized"
- Make sure Node.js is installed
- Restart your computer after installing Node.js

### Batch file won't run / shows security warning
- Right-click the .bat file → Properties
- Click "Unblock" if you see it → Apply → OK
- Try running again

### Port already in use
- Close any other applications using ports 8000 or 3000
- OR run `STOP_APP.bat` first
- OR restart your computer

### Dependencies not installing
- Make sure you have internet connection
- Run `SETUP.bat` as Administrator:
  - Right-click `SETUP.bat`
  - Choose "Run as administrator"

---

## 💡 Tips

**Create a Desktop Shortcut:**
1. Right-click `START_APP.bat`
2. Choose "Create shortcut"
3. Drag the shortcut to your Desktop
4. Rename it to "Sports Medicine App"
5. Now you can launch from your desktop!

**Pin to Taskbar:**
1. Create a shortcut (see above)
2. Right-click the shortcut
3. Choose "Pin to taskbar"

---

## 📊 What You'll See When Running

### START_APP.bat Output:
```
========================================
Sports Medicine - Injury Prevention System
========================================

Starting application...

========================================
Starting Backend Server...
========================================
[New window opens with backend server]

========================================
Starting Frontend Server...
========================================
[New window opens with frontend server]

Application is starting!
Backend will open at:  http://localhost:8000
Frontend will open at: http://localhost:3000

[Browser opens automatically]
```

### Two Terminal Windows:
1. **Backend Window**: Shows API logs and database activity
2. **Frontend Window**: Shows Vite dev server

**Keep both windows open** while using the application!

---

## 🛑 Stopping the Application

**Method 1: Close Windows**
- Close both terminal windows manually
- Click the X on each window

**Method 2: Use STOP_APP.bat**
- Double-click `STOP_APP.bat`
- Everything stops automatically

**Method 3: Ctrl+C**
- In each terminal window, press `Ctrl+C`
- Confirm when asked

---

## 🆘 Need Help?

If launchers don't work, you can always run manually:

**Manual Backend:**
```cmd
cd C:\path\to\sports_medicine
venv\Scripts\activate
python run_backend.py
```

**Manual Frontend (new window):**
```cmd
cd C:\path\to\sports_medicine\frontend
npm run dev
```

---

## ✅ Success Indicators

**Backend is running when you see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
Initializing database...
Database initialized successfully!
```

**Frontend is running when you see:**
```
VITE v5.x.x  ready in xxx ms
➜  Local:   http://localhost:3000/
```

**Application is working when:**
- Browser opens to http://localhost:3000
- You see the "Sports Medicine - Injury Prevention System" page
- Navigation menu shows: Team Dashboard, Manage Athletes, Upload Data

---

Happy coaching! 🏃‍♂️💪
