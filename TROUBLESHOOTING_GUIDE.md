# 🔧 Troubleshooting Guide
## "Failed to load athletes: Network Error"

This error means the frontend can't connect to the backend server. Follow these steps in order:

---

## ✅ Step 1: Verify Backend Is Running

**Look at your Backend terminal window.** You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
Initializing database...
Database initialized successfully!
```

### If you DON'T see this:
1. Close both terminal windows
2. Run **START_APP.bat** again
3. Wait for both windows to fully load

### If backend window shows errors:
- Check that Python is installed: Open Command Prompt and type `python --version`
- Make sure you ran **SETUP.bat** first
- Try running **SETUP.bat** again

---

## ✅ Step 2: Test Backend Connection

1. Open a new browser tab
2. Go to: **http://127.0.0.1:8000**
3. You should see JSON like this:
   ```json
   {
     "message": "Sports Medicine - Injury Prevention System API",
     "version": "1.0.0",
     "docs": "/docs",
     "status": "running"
   }
   ```

### If you see the JSON:
✅ Backend is working! Continue to Step 3.

### If you see "This site can't be reached":
❌ Backend isn't running or is on wrong port.

**Fix:**
1. Close all terminal windows
2. Double-click **STOP_APP.bat**
3. Wait 10 seconds
4. Double-click **START_APP.bat** again

---

## ✅ Step 3: Restart Both Servers

**This fixes 90% of connection issues:**

1. Close both terminal windows (Backend and Frontend)
2. Wait 5 seconds
3. Double-click **START_APP.bat**
4. Wait for both windows to open
5. Wait 10 seconds for servers to fully start
6. Refresh your browser (F5)

---

## ✅ Step 4: Check Windows Firewall

Windows Firewall might be blocking the connection.

1. Press **Windows Key**
2. Type "**Windows Defender Firewall**"
3. Click "**Allow an app through Windows Firewall**"
4. Look for "**Python**" in the list
5. Make sure both **Private** and **Public** checkboxes are checked
6. Click **OK**
7. Restart the application

---

## ✅ Step 5: Try Different URLs

The frontend might be connecting to the wrong URL.

### Test these URLs in your browser:

1. **http://127.0.0.1:8000** (Should show JSON)
2. **http://localhost:8000** (Should show JSON)
3. **http://127.0.0.1:3000** (Should show the app)
4. **http://localhost:3000** (Should show the app)

### Which one works?
- If **127.0.0.1:8000** works: You're good! ✅
- If only **localhost:8000** works: Need to reconfigure
- If neither works: Backend isn't running

---

## ✅ Step 6: Clear Browser Cache

Sometimes old data causes issues.

**Chrome/Edge:**
1. Press **Ctrl + Shift + Delete**
2. Select "**Cached images and files**"
3. Click "**Clear data**"
4. Refresh the page (F5)

**Or use Incognito:**
1. Press **Ctrl + Shift + N**
2. Go to **http://127.0.0.1:3000**

---

## ✅ Step 7: Check for Port Conflicts

Another program might be using ports 8000 or 3000.

### Run the troubleshoot script:
1. Double-click **TROUBLESHOOT.bat**
2. It will show which ports are in use

### If ports are blocked:
1. Find and close the program using the port
2. Or restart your computer
3. Run **START_APP.bat** again

---

## ✅ Step 8: Reinstall Dependencies

Dependencies might be corrupted.

1. Close all terminal windows
2. Delete these folders (if they exist):
   - `venv`
   - `frontend\node_modules`
3. Double-click **SETUP.bat**
4. Wait for installation (5-10 minutes)
5. Double-click **START_APP.bat**

---

## ✅ Step 9: Check Python/Node.js Installation

### Check Python:
```cmd
python --version
```
Should show: `Python 3.9.x` or higher

### Check Node.js:
```cmd
node --version
npm --version
```
Should show version numbers

### If not installed:
- **Python**: Download from https://python.org (check "Add to PATH")
- **Node.js**: Download from https://nodejs.org
- Restart computer after installing
- Run **SETUP.bat** again

---

## ✅ Step 10: Manual Start (Advanced)

If launchers don't work, start manually:

### Terminal 1 - Backend:
```cmd
cd C:\path\to\sports_medicine
venv\Scripts\activate
python run_backend.py
```
Wait for: `Uvicorn running on http://127.0.0.1:8000`

### Terminal 2 - Frontend (new window):
```cmd
cd C:\path\to\sports_medicine\frontend
npm run dev
```
Wait for: `Local: http://localhost:3000`

### Then:
Open browser to **http://127.0.0.1:3000** or **http://localhost:3000**

---

## 🔥 Nuclear Option: Complete Reset

If nothing else works:

1. **Uninstall and Reinstall:**
   - Uninstall Python
   - Uninstall Node.js
   - Restart computer
   - Reinstall Python (CHECK "Add to PATH")
   - Reinstall Node.js
   - Restart computer again

2. **Fresh Download:**
   - Delete the entire `sports_medicine` folder
   - Download fresh from GitHub
   - Extract to new location
   - Run **SETUP.bat**
   - Run **START_APP.bat**

3. **Disable Antivirus Temporarily:**
   - Some antivirus software blocks local servers
   - Temporarily disable it
   - Try running the app
   - Re-enable antivirus after testing

---

## 📋 Common Error Messages

### "Port 8000 is already in use"
**Solution:** Run **STOP_APP.bat** or restart computer

### "Module not found"
**Solution:** Run **SETUP.bat** again

### "Python is not recognized"
**Solution:** Reinstall Python and check "Add to PATH"

### "npm is not recognized"
**Solution:** Reinstall Node.js

### Backend window closes immediately
**Solution:** Check for errors in the window before it closes. Run manually to see errors:
```cmd
cd C:\path\to\sports_medicine
venv\Scripts\activate
python run_backend.py
```

---

## 🆘 Still Not Working?

### Check the Backend Logs

Look in the Backend terminal window for errors. Common ones:

**"Address already in use"** → Port 8000 blocked. Run STOP_APP.bat

**"ModuleNotFoundError"** → Dependencies missing. Run SETUP.bat

**"Permission denied"** → Run as Administrator

**"Database locked"** → Delete `sports_medicine.db` file and restart

### Check the Frontend Logs

Look in the Frontend terminal window for errors:

**"EADDRINUSE"** → Port 3000 blocked. Close other apps

**"Module not found"** → Run `npm install` in frontend folder

**"Failed to compile"** → Check for syntax errors in code

---

## 💡 Prevention Tips

1. **Always use the launchers** (START_APP.bat)
2. **Don't close terminal windows** while using the app
3. **Use STOP_APP.bat** to cleanly shut down
4. **Keep Windows updated**
5. **Don't move files** while app is running
6. **Run SETUP.bat** if you update from GitHub

---

## ✅ Success Checklist

- [ ] Backend window shows "Uvicorn running"
- [ ] Frontend window shows "Local: http://localhost:3000"
- [ ] http://127.0.0.1:8000 shows JSON response
- [ ] http://127.0.0.1:3000 shows the application
- [ ] No firewall warnings
- [ ] Both terminal windows stay open
- [ ] You can navigate between pages without errors

---

## 📞 Getting More Help

If you've tried everything:

1. Take screenshots of:
   - Backend terminal window
   - Frontend terminal window
   - Browser error (F12 → Console tab)

2. Note which steps you've tried

3. Check if antivirus/firewall is blocking

4. Try on a different computer to rule out system issues

---

**Most issues are fixed by:**
1. Running **STOP_APP.bat**
2. Waiting 10 seconds
3. Running **START_APP.bat** again
4. Waiting for both servers to fully start
5. Refreshing browser

Good luck! 🍀
