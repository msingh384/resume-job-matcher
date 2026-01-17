# ⚠️ PORT CHANGED: 5000 → 8000

## 🔍 What Happened

Your tests were failing because **Apple's AirPlay Receiver** was using port 5000, preventing your Flask backend from starting!

**Error seen:**
```
HTTP/1.1 403 Forbidden
Server: AirTunes/755.3.1
```

This is a common issue on macOS where AirPlay uses port 5000 by default.

## ✅ What Was Fixed

I've updated your application to use **port 8000** instead:

### Files Updated:
- ✅ `backend/app.py` - Now runs on port 8000
- ✅ `test_app.sh` - Tests now check port 8000
- ✅ `frontend/vite.config.js` - Frontend proxy now points to port 8000
- ✅ `docker-compose.yml` - Docker maps port 8000
- ✅ `Dockerfile` - Exposes port 8000
- ✅ Added `punkt_tab` to NLTK downloads

## 🚀 How to Test NOW

### Option 1: Stop and Restart Backend

If your backend is currently running:

1. **Stop it**: Press `Ctrl+C` in the terminal running the backend

2. **Restart it**:
   ```bash
   cd /Users/mannanrajsingh/resume-job-matcher
   source venv/bin/activate
   python backend/app.py
   ```

3. **You should see**:
   ```
   ==================================================
   Resume-Job Matcher Server
   ==================================================
   Mode: TF-IDF
   Open http://localhost:8000 in your browser
   ==================================================
    * Serving Flask app 'app'
    * Debug mode: on
    * Running on http://127.0.0.1:8000
   ```

4. **Run tests** (in a new terminal):
   ```bash
   cd /Users/mannanrajsingh/resume-job-matcher
   ./test_app.sh
   ```

### Option 2: Use Docker

```bash
cd /Users/mannanrajsingh/resume-job-matcher
docker-compose up --build
```

Open: **http://localhost:8000**

## 📝 Important URLs Changed

| Old URL | New URL |
|---------|---------|
| `http://localhost:5000` | `http://localhost:8000` |
| `http://localhost:5000/api/status` | `http://localhost:8000/api/status` |

## 🍎 Alternative: Disable AirPlay (Optional)

If you prefer to keep port 5000, you can disable AirPlay Receiver:

1. Open **System Settings**
2. Go to **General** → **AirDrop & Handoff**
3. Turn off **AirPlay Receiver**

Then revert the port back to 5000 in all files.

## ✅ Expected Test Results

After restarting the backend on port 8000, run `./test_app.sh`:

```
🧪 Resume-Job Matcher - Automated Test Suite
==============================================

1️⃣  Checking if server is running...
✓ Server is running

2️⃣  Testing API Endpoints...
✓ GET /api/status

3️⃣  Testing Resume Upload...
✓ POST /api/upload-resume
✓ Resume upload verified

... (more tests)

==============================================
📊 Test Summary
==============================================
Tests Run:    19
Tests Passed: 19
Tests Failed: 0

🎉 All tests passed! Application is working correctly.
```

## 🎯 Next Steps

1. **Restart your backend** on port 8000
2. **Run the tests** - `./test_app.sh`
3. **Test in browser** - Open http://localhost:8000
4. **All should work!** ✅

---

**Need Help?**

If tests still fail after restarting on port 8000:
1. Check backend logs for errors
2. Ensure port 8000 is available: `lsof -i :8000`
3. Review [TESTING.md](TESTING.md) for troubleshooting

