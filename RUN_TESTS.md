# 🚀 Quick Test & Run Guide

Fast reference for testing and running the Resume-Job Matcher application.

## 🏃 Quick Start - Test Everything in 5 Minutes

### Option 1: Run with Docker (Easiest - Recommended for Testing Production)

```bash
# Build and start the application
docker-compose up --build

# Open in browser
open http://localhost:5000

# In another terminal, test the endpoints
curl http://localhost:5000/api/status

# Stop when done
docker-compose down
```

### Option 2: Run Locally (Best for Development)

```bash
# Terminal 1 - Start Backend
source venv/bin/activate
python backend/app.py

# Terminal 2 - Run Automated Tests
./test_app.sh

# Terminal 3 - Start Frontend (Optional for dev)
cd frontend
npm run dev
# Access at http://localhost:3000
```

---

## 🧪 Automated Testing

### Run the Test Suite

```bash
# Make sure backend is running first
source venv/bin/activate
python backend/app.py

# In another terminal, run tests
./test_app.sh
```

**Expected Output:**
```
🧪 Resume-Job Matcher - Automated Test Suite
==============================================

1️⃣  Checking if server is running...
✓ Server is running

2️⃣  Testing API Endpoints...
Testing GET /api/status...
✓ GET /api/status

3️⃣  Testing Resume Upload...
Creating test resume...
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

---

## ✅ Manual Testing Checklist

### Quick 5-Minute Smoke Test

1. **Start the application** (Docker or local)

2. **Open browser** to http://localhost:5000

3. **Test Resume Upload:**
   - Click or drag a resume file (PDF/DOCX/TXT)
   - Verify success message appears
   - Check filename displays

4. **Test Add Job:**
   - Click "Add Job" button
   - Fill in:
     - Title: "Full Stack Developer"
     - Company: "Tech Corp"
     - Description: "Looking for Python, React, Docker skills"
     - URL: "https://example.com/job"
   - Click "Add Job"
   - Verify job card appears with match score

5. **Test Match Details:**
   - Click "View Details" on the job
   - Verify modal shows:
     - Match score (percentage)
     - Missing keywords list
     - Recommendations
     - Full job description

6. **Test Status Update:**
   - Click status dropdown on job card
   - Change to "Applied"
   - Verify badge color changes
   - Verify statistics update

7. **Test Delete:**
   - Click trash icon on job
   - Verify job disappears
   - Verify statistics update

**If all work: ✅ Application is ready!**

---

## 🔍 Verify Production Readiness

### Checklist Before Deployment

```bash
# 1. Run automated tests
./test_app.sh
# Expected: All tests pass

# 2. Test Docker build
docker-compose build
# Expected: Build succeeds without errors

# 3. Test Docker run
docker-compose up
# Expected: Application starts and is accessible

# 4. Test health check
curl http://localhost:5000/api/status
# Expected: {"has_resume": false, "ml_mode": false, "matcher_type": "TF-IDF"}

# 5. Test data persistence
# - Add a job
# - Stop container: docker-compose down
# - Restart: docker-compose up
# - Verify job still exists
```

---

## 📊 Quick API Tests with curl

### Test All Endpoints

```bash
# 1. Check Status
curl http://localhost:5000/api/status

# 2. Upload Resume
echo "John Doe, Software Engineer with Python and React skills" > resume.txt
curl -X POST -F "file=@resume.txt" http://localhost:5000/api/upload-resume

# 3. Add Job
curl -X POST http://localhost:5000/api/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Software Engineer",
    "company": "Tech Co",
    "description": "Python and React developer needed",
    "url": "https://example.com/job"
  }'

# 4. List Jobs
curl http://localhost:5000/api/jobs

# 5. Get Job Details (replace 1 with actual job ID)
curl http://localhost:5000/api/jobs/1

# 6. Update Job Status
curl -X PUT http://localhost:5000/api/jobs/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "applied"}'

# 7. Get Match Details
curl http://localhost:5000/api/match/1

# 8. Delete Job
curl -X DELETE http://localhost:5000/api/jobs/1
```

---

## 🐛 Troubleshooting

### Backend Won't Start

```bash
# Check Python version
python3 --version  # Need 3.8+

# Reinstall dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Check if port is available
lsof -i :5000
```

### Tests Failing

```bash
# Make sure backend is running
ps aux | grep python

# Check backend URL
curl http://localhost:5000/api/status

# View backend logs
# Check terminal where backend is running
```

### Docker Issues

```bash
# Clean everything and rebuild
docker-compose down -v
docker system prune -a
docker-compose up --build

# View logs
docker-compose logs -f

# Check container status
docker-compose ps
```

### Frontend Not Connecting

```bash
# Check if backend is running
curl http://localhost:5000/api/status

# Check frontend dev server
cd frontend
npm install
npm run dev

# Try accessing directly
open http://localhost:5000  # Served by backend
open http://localhost:3000  # Dev server
```

---

## 📈 Performance Tests (Optional)

### Test with Multiple Jobs

```bash
# Add 10 jobs
for i in {1..10}; do
  curl -X POST http://localhost:5000/api/jobs \
    -H "Content-Type: application/json" \
    -d "{\"title\": \"Job $i\", \"company\": \"Company $i\", \"description\": \"Looking for experienced developer with Python skills\"}"
done

# Check performance
time curl http://localhost:5000/api/jobs
```

### Test Large Resume

```bash
# Create a large resume (multiple pages)
cat > large_resume.txt << 'EOF'
[Paste your actual multi-page resume here]
EOF

# Upload and measure time
time curl -X POST -F "file=@large_resume.txt" http://localhost:5000/api/upload-resume
```

---

## ✅ Success Criteria

Your application is working if:

✅ **Backend Tests:**
- Server starts without errors
- All API endpoints return proper responses
- Resume upload succeeds
- Jobs can be added, updated, deleted
- Match scores calculate correctly

✅ **Frontend Tests:**
- UI loads without errors
- Resume upload works with drag-and-drop
- Jobs display correctly
- Match details modal works
- Status updates work
- Statistics update correctly

✅ **Docker Tests:**
- Container builds successfully
- Application runs in Docker
- Health check passes
- Data persists after restart

✅ **Integration Tests:**
- Complete workflow works end-to-end
- No console errors
- Smooth user experience

---

## 🎯 Next Steps

After all tests pass:

1. **Review** the detailed [TESTING.md](TESTING.md) for comprehensive testing
2. **Read** [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
3. **Deploy** to your preferred platform
4. **Monitor** using the health check endpoint
5. **Backup** your data directory regularly

---

## 🆘 Getting Help

If tests fail or you encounter issues:

1. **Check Logs:**
   - Backend: Look at terminal where `python backend/app.py` is running
   - Docker: Run `docker-compose logs -f`

2. **Review Documentation:**
   - [README.md](README.md) - Full documentation
   - [TESTING.md](TESTING.md) - Detailed testing guide
   - [QUICKSTART.md](QUICKSTART.md) - Setup guide

3. **Common Issues:**
   - Port conflicts: Kill process using port 5000
   - Missing dependencies: Run `pip install -r requirements.txt`
   - NLTK data: Run `python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"`

4. **Still Stuck:**
   - Check GitHub issues
   - Open a new issue with logs

---

**Ready to test? Run: `./test_app.sh` 🚀**

