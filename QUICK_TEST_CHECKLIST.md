# ✅ Quick Test Checklist

Use this checklist to verify your Resume-Job Matcher is production-ready.

## 🎯 Pre-Test Setup

```bash
# Navigate to project
cd /Users/mannanrajsingh/resume-job-matcher

# Activate virtual environment
source venv/bin/activate

# Start backend
python backend/app.py
```

---

## 📋 Testing Checklist

### ✅ Backend Tests (5 minutes)

In a new terminal:

```bash
cd /Users/mannanrajsingh/resume-job-matcher
./test_app.sh
```

- [ ] All 19 automated tests pass
- [ ] Server responds to `/api/status`
- [ ] Resume upload works
- [ ] Job CRUD operations work
- [ ] Match scoring works
- [ ] Error handling works

**Expected:** `Tests Passed: 19, Tests Failed: 0`

---

### ✅ Frontend/UI Tests (5 minutes)

Open browser to **http://localhost:5000**

#### Resume Upload
- [ ] Drag and drop works
- [ ] Click to browse works
- [ ] Success message appears
- [ ] Filename displays
- [ ] Works with PDF files
- [ ] Works with DOCX files
- [ ] Works with TXT files
- [ ] Error shown for invalid files

#### Add Job
- [ ] "Add Job" button opens modal
- [ ] All fields can be filled
- [ ] Form validation works
- [ ] Job appears after adding
- [ ] Match score displays
- [ ] Color coding correct (Great/Good/Fair)

#### Job List
- [ ] Jobs display in cards
- [ ] Match scores visible
- [ ] Status badges show
- [ ] Missing keywords display
- [ ] Jobs sorted by match score

#### Match Details
- [ ] "View Details" opens modal
- [ ] Match score shows correctly
- [ ] Circular progress indicator works
- [ ] Missing keywords listed
- [ ] Recommendations appear
- [ ] Full job description displays
- [ ] Modal closes properly

#### Update Status
- [ ] Status dropdown works
- [ ] Can change to "Applied"
- [ ] Can change to "Interview"
- [ ] Can change to "Offer"
- [ ] Can change to "Rejected"
- [ ] Badge color updates
- [ ] Statistics update

#### Delete Job
- [ ] Trash icon clickable
- [ ] Job removes from list
- [ ] Statistics update
- [ ] No errors in console

#### Dashboard Statistics
- [ ] Total Jobs count accurate
- [ ] Average Match Score accurate
- [ ] Applications count accurate
- [ ] Interviews count accurate
- [ ] Updates in real-time

---

### ✅ Docker Tests (5 minutes)

Stop local backend (Ctrl+C), then:

```bash
docker-compose up --build
```

- [ ] Docker build succeeds
- [ ] Container starts without errors
- [ ] Application accessible at http://localhost:5000
- [ ] All UI features work
- [ ] Can upload resume
- [ ] Can add/update/delete jobs

#### Data Persistence Test
```bash
# 1. Add a job in browser
# 2. Stop container
docker-compose down

# 3. Restart
docker-compose up

# 4. Check browser - job should still exist
```

- [ ] Data persists after restart
- [ ] Database file in `data/` directory

---

### ✅ API Tests (Optional - 5 minutes)

Test endpoints with curl:

```bash
# Status
curl http://localhost:5000/api/status
# [ ] Returns JSON with status

# Upload Resume
echo "Test Resume Content" > test.txt
curl -X POST -F "file=@test.txt" http://localhost:5000/api/upload-resume
# [ ] Returns success message

# Add Job
curl -X POST http://localhost:5000/api/jobs \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","company":"Co","description":"Python React"}'
# [ ] Returns job with match_score

# List Jobs
curl http://localhost:5000/api/jobs
# [ ] Returns array of jobs

# Get Job
curl http://localhost:5000/api/jobs/1
# [ ] Returns single job

# Update Job
curl -X PUT http://localhost:5000/api/jobs/1 \
  -H "Content-Type: application/json" \
  -d '{"status":"applied"}'
# [ ] Returns updated job

# Match Details
curl http://localhost:5000/api/match/1
# [ ] Returns match analysis

# Delete Job
curl -X DELETE http://localhost:5000/api/jobs/1
# [ ] Returns success message
```

---

### ✅ Performance Tests (Optional - 2 minutes)

```bash
# Add 20 jobs quickly
for i in {1..20}; do
  curl -s -X POST http://localhost:5000/api/jobs \
    -H "Content-Type: application/json" \
    -d "{\"title\":\"Job $i\",\"company\":\"Co\",\"description\":\"Python\"}" &
done
wait

# Check response time
time curl http://localhost:5000/api/jobs
```

- [ ] Can handle multiple jobs
- [ ] Response time < 1 second
- [ ] No errors or crashes
- [ ] UI remains responsive

---

### ✅ Error Handling Tests (2 minutes)

#### Backend Errors
```bash
# No file
curl -X POST http://localhost:5000/api/upload-resume
# [ ] Returns error message

# Invalid job
curl -X POST http://localhost:5000/api/jobs \
  -H "Content-Type: application/json" -d '{}'
# [ ] Returns error message

# Non-existent job
curl http://localhost:5000/api/jobs/99999
# [ ] Returns 404 error
```

#### Frontend Errors
- [ ] Try uploading 100MB file → Shows error
- [ ] Try uploading .exe file → Shows error
- [ ] Try adding job without title → Shows validation
- [ ] Network error handling works

---

## 🎉 Success Criteria

### Minimum Requirements (Must Pass)
- ✅ All automated tests pass (19/19)
- ✅ Backend starts without errors
- ✅ UI loads and is responsive
- ✅ Resume upload works
- ✅ Job CRUD operations work
- ✅ Match scoring calculates
- ✅ Docker build succeeds
- ✅ Docker container runs

### Production Ready (Recommended)
- ✅ All minimum requirements met
- ✅ Data persists after restart
- ✅ Error handling works properly
- ✅ Performance is acceptable
- ✅ No console errors
- ✅ Mobile responsive (bonus)
- ✅ Documentation complete

---

## 📊 Test Results Template

```
# Test Results - [Date]

## Environment
- OS: macOS 23.3.0
- Python: [version]
- Node: [version]
- Docker: [version]

## Results
- Backend Tests: ✅ 19/19 passed
- Frontend Tests: ✅ All features work
- Docker Tests: ✅ Build and run successful
- Data Persistence: ✅ Verified
- API Tests: ✅ All endpoints respond
- Performance: ✅ Acceptable
- Error Handling: ✅ Working

## Issues Found
[None / List any issues]

## Status
✅ PRODUCTION READY

Tested by: [Your Name]
Date: [Date]
```

---

## 🚀 After All Tests Pass

1. **Document Results:** Fill out test results template above
2. **Review Deployment:** Read [DEPLOYMENT.md](DEPLOYMENT.md)
3. **Choose Platform:** Select deployment target
4. **Deploy:** Follow deployment guide
5. **Monitor:** Set up health checks
6. **Backup:** Configure database backups

---

## 🐛 If Tests Fail

### Backend Issues
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Check port
lsof -i :5000
```

### Frontend Issues
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Docker Issues
```bash
docker-compose down -v
docker system prune -a
docker-compose up --build
```

### Still Having Issues?
1. Check [TESTING.md](TESTING.md) for detailed troubleshooting
2. Review logs carefully
3. Search GitHub issues
4. Open new issue with details

---

## 📚 Additional Resources

- **[START_HERE.md](START_HERE.md)** - Guided walkthrough
- **[RUN_TESTS.md](RUN_TESTS.md)** - Quick command reference
- **[TESTING.md](TESTING.md)** - Comprehensive testing guide
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment
- **[README.md](README.md)** - Full documentation

---

**Print this checklist and check off items as you test! 📋✅**

