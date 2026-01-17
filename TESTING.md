# 🧪 Testing Guide - Resume-Job Matcher

This guide will help you thoroughly test the application before production deployment.

## 📋 Pre-Deployment Checklist

### ✅ Environment Setup

- [ ] Python 3.8+ installed (`python3 --version`)
- [ ] Node.js 16+ installed (`node --version`)
- [ ] Docker & Docker Compose installed (for production deployment)
- [ ] All dependencies installed
- [ ] NLTK data downloaded

### ✅ Backend Tests

- [ ] Backend starts without errors
- [ ] Database initializes correctly
- [ ] API endpoints respond
- [ ] Resume upload works (PDF, DOCX, TXT)
- [ ] Job CRUD operations work
- [ ] Match scoring calculates correctly
- [ ] Keyword gap analysis works

### ✅ Frontend Tests

- [ ] Frontend builds successfully
- [ ] UI loads without errors
- [ ] All components render
- [ ] API calls work correctly
- [ ] File upload UI works
- [ ] Modal interactions work
- [ ] Status updates work

### ✅ Integration Tests

- [ ] Full workflow: Upload resume → Add job → View match
- [ ] Mode switching (TF-IDF ↔ ML) works
- [ ] Data persistence after restart
- [ ] Error handling displays correctly

### ✅ Production Tests

- [ ] Docker build succeeds
- [ ] Docker container runs
- [ ] Health checks pass
- [ ] Production build is optimized
- [ ] Static files serve correctly

---

## 🚀 Quick Test Methods

### Method 1: Automated Test Script

Run the provided test script to check all endpoints:

```bash
# Make executable
chmod +x test_app.sh

# Run tests
./test_app.sh
```

### Method 2: Manual Testing (Recommended)

Follow the detailed steps below for comprehensive testing.

---

## 📝 Detailed Manual Testing Guide

### 1️⃣ Backend Testing

#### Step 1: Start the Backend

```bash
# Activate virtual environment
source venv/bin/activate

# Start backend
python backend/app.py
```

**Expected Output:**
```
==================================================
Resume-Job Matcher Server
==================================================
Mode: TF-IDF
Open http://localhost:5000 in your browser
==================================================
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

#### Step 2: Test API Endpoints

**Test Status Endpoint:**
```bash
curl http://localhost:5000/api/status
```
Expected: `{"has_resume": false, "ml_mode": false, "matcher_type": "TF-IDF"}`

**Test Resume Upload:**
```bash
# Create a test resume file
echo "John Doe\nSoftware Engineer\nSkills: Python, React, Docker, Flask, JavaScript" > test_resume.txt

# Upload it
curl -X POST -F "file=@test_resume.txt" http://localhost:5000/api/upload-resume
```
Expected: Success message with preview

**Test Add Job:**
```bash
curl -X POST http://localhost:5000/api/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Full Stack Developer",
    "company": "Tech Corp",
    "description": "Looking for a developer with Python, React, and Docker experience.",
    "url": "https://example.com/job"
  }'
```
Expected: Job object with match_score

**Test Get Jobs:**
```bash
curl http://localhost:5000/api/jobs
```
Expected: Array of jobs with match scores

**Test Update Job Status:**
```bash
curl -X PUT http://localhost:5000/api/jobs/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "applied"}'
```
Expected: Updated job object

**Test Get Match Details:**
```bash
curl http://localhost:5000/api/match/1
```
Expected: Match details with keyword gaps

**Test Delete Job:**
```bash
curl -X DELETE http://localhost:5000/api/jobs/1
```
Expected: Success message

---

### 2️⃣ Frontend Testing

#### Step 1: Start Frontend (new terminal)

```bash
cd frontend
npm run dev
```

**Expected Output:**
```
VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

#### Step 2: Manual UI Testing

Open http://localhost:3000 in your browser and test:

**Resume Upload:**
- [ ] Drag and drop a resume file
- [ ] Click to browse and select file
- [ ] See upload progress/success message
- [ ] Verify file name appears
- [ ] Test with PDF, DOCX, and TXT files
- [ ] Test error handling with invalid file

**Add Job:**
- [ ] Click "Add Job" button
- [ ] Modal opens smoothly
- [ ] Fill in all fields (title, company, description, URL)
- [ ] Submit and see job appear
- [ ] Verify match score appears
- [ ] Check color coding (Great/Good/Fair)

**Job List:**
- [ ] Jobs display correctly
- [ ] Match scores show properly
- [ ] Status badges work
- [ ] Sorting works (by match score)
- [ ] Missing keywords display

**View Match Details:**
- [ ] Click "View Details" on a job
- [ ] Modal opens with match analysis
- [ ] Circular progress indicator shows score
- [ ] Missing keywords listed
- [ ] Recommendations appear
- [ ] Job description displays

**Update Job Status:**
- [ ] Click status dropdown
- [ ] Change to "Applied"
- [ ] Change to "Interview"
- [ ] Change to "Offer"
- [ ] Badge color updates
- [ ] Statistics update

**Delete Job:**
- [ ] Click delete button (trash icon)
- [ ] Confirm deletion
- [ ] Job removes from list
- [ ] Statistics update

**Dashboard Statistics:**
- [ ] Total Jobs count accurate
- [ ] Average Match Score accurate
- [ ] Applications count accurate
- [ ] Interviews count accurate

---

### 3️⃣ Docker/Production Testing

#### Step 1: Build Docker Image

```bash
docker-compose build
```

**Expected:** Build succeeds without errors

#### Step 2: Run Docker Container

```bash
docker-compose up
```

**Expected Output:**
```
resume-job-matcher-app-1  | ==================================================
resume-job-matcher-app-1  | Resume-Job Matcher Server
resume-job-matcher-app-1  | ==================================================
resume-job-matcher-app-1  | Mode: TF-IDF
resume-job-matcher-app-1  | Open http://localhost:5000 in your browser
```

#### Step 3: Test Production Build

Open http://localhost:5000 and verify:

- [ ] Application loads
- [ ] Static files serve correctly
- [ ] All features work
- [ ] Upload/download works
- [ ] Data persists after restart

#### Step 4: Test Health Check

```bash
curl http://localhost:5000/api/status
```

Expected: Successful response

#### Step 5: Test Data Persistence

```bash
# Upload resume and add job
# Stop container
docker-compose down

# Restart
docker-compose up

# Verify data still exists
curl http://localhost:5000/api/jobs
```

Expected: Previously added jobs still present

---

## 🔍 Common Issues & Solutions

### Issue: Backend won't start

**Symptoms:**
- Import errors
- NLTK data not found
- Port already in use

**Solutions:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Check port
lsof -i :5000
# Kill process if needed
kill -9 <PID>
```

### Issue: Frontend won't start

**Symptoms:**
- Module not found errors
- Port conflict

**Solutions:**
```bash
# Clean install
rm -rf node_modules package-lock.json
npm install

# Use different port
npm run dev -- --port 3001
```

### Issue: Resume upload fails

**Symptoms:**
- Error parsing PDF
- File too large
- Unsupported format

**Solutions:**
- Check file size (max 16MB)
- Verify file format (PDF/DOCX/TXT)
- Try different PDF (some PDFs have encryption)
- Check backend logs for specific error

### Issue: Match scores not calculating

**Symptoms:**
- Score shows 0 or null
- Missing keywords empty

**Solutions:**
- Ensure resume uploaded first
- Check resume has content (not blank)
- Verify job description not empty
- Check backend logs for errors

### Issue: Docker build fails

**Symptoms:**
- Dependency installation errors
- Build context too large

**Solutions:**
```bash
# Clean Docker
docker system prune -a

# Rebuild
docker-compose build --no-cache

# Check .dockerignore exists
```

---

## 🎯 Performance Testing

### Load Testing (Optional)

Test with multiple jobs:

```bash
# Add 50 jobs
for i in {1..50}; do
  curl -X POST http://localhost:5000/api/jobs \
    -H "Content-Type: application/json" \
    -d "{\"title\": \"Job $i\", \"company\": \"Company $i\", \"description\": \"Looking for developer with skills\"}"
done

# Measure response time
time curl http://localhost:5000/api/jobs
```

### Large Resume Test

Test with a large resume (5-10 pages):
- Upload should complete within 5 seconds
- Parsing should succeed
- Match calculations should be fast (<1s per job)

---

## ✅ Production Readiness Checklist

Before deploying to production:

### Code Quality
- [ ] No console.log in production frontend code
- [ ] No debug mode in production backend
- [ ] Error handling for all user inputs
- [ ] Proper HTTP status codes
- [ ] Input validation on backend

### Security
- [ ] File upload size limits enforced
- [ ] File type validation
- [ ] No sensitive data in logs
- [ ] CORS configured correctly
- [ ] SQL injection prevention (using parameterized queries)

### Performance
- [ ] Frontend build optimized (run `npm run build`)
- [ ] Static assets compressed
- [ ] Database queries efficient
- [ ] Large file handling works
- [ ] Memory leaks checked

### Monitoring
- [ ] Health check endpoint works
- [ ] Error logging in place
- [ ] Application logs accessible

### Documentation
- [ ] README up to date
- [ ] API documentation accurate
- [ ] Environment variables documented
- [ ] Deployment instructions clear

### Data
- [ ] Database backup strategy
- [ ] Data directory persistent (Docker volume)
- [ ] Migration strategy if needed

### Deployment
- [ ] Docker build succeeds
- [ ] Environment variables set
- [ ] Restart policy configured
- [ ] Health checks configured
- [ ] Port mapping correct

---

## 🎉 Success Criteria

Your application is production-ready when:

✅ All automated tests pass
✅ Manual testing completes without errors
✅ Docker container runs successfully
✅ Data persists after restart
✅ Health checks pass
✅ Performance is acceptable
✅ Error handling works properly
✅ Documentation is complete

---

## 📊 Test Report Template

After testing, document your results:

```
# Test Report - [Date]

## Environment
- OS: [Your OS]
- Python Version: [Version]
- Node Version: [Version]
- Docker Version: [Version]

## Backend Tests
- Status Endpoint: ✅/❌
- Resume Upload: ✅/❌
- Job CRUD: ✅/❌
- Match Scoring: ✅/❌

## Frontend Tests
- UI Load: ✅/❌
- Resume Upload UI: ✅/❌
- Job Management: ✅/❌
- Match Details: ✅/❌

## Docker Tests
- Build: ✅/❌
- Run: ✅/❌
- Health Check: ✅/❌
- Data Persistence: ✅/❌

## Issues Found
[List any issues]

## Resolution Status
[How issues were resolved]

## Sign-off
Tested by: [Your Name]
Date: [Date]
Status: ✅ Ready for Production / ❌ Needs Work
```

---

**Ready to deploy? 🚀**

See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment instructions!

