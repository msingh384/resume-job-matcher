#!/bin/bash

# Resume-Job Matcher - Automated Test Script
# This script tests all API endpoints and basic functionality

echo "🧪 Resume-Job Matcher - Automated Test Suite"
echo "=============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Base URL
BASE_URL="http://localhost:8000"

# Function to print test result
print_result() {
    local test_name=$1
    local result=$2
    
    TESTS_RUN=$((TESTS_RUN + 1))
    
    if [ "$result" = "PASS" ]; then
        echo -e "${GREEN}✓${NC} $test_name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗${NC} $test_name"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# Check if server is running
echo "1️⃣  Checking if server is running..."
if curl -s "$BASE_URL/api/status" > /dev/null 2>&1; then
    print_result "Server is running" "PASS"
else
    print_result "Server is running" "FAIL"
    echo ""
    echo -e "${RED}❌ Server is not running!${NC}"
    echo "Please start the backend server first:"
    echo "  source venv/bin/activate"
    echo "  python backend/app.py"
    exit 1
fi

echo ""
echo "2️⃣  Testing API Endpoints..."

# Test 1: Get Status
echo "Testing GET /api/status..."
response=$(curl -s "$BASE_URL/api/status")
if echo "$response" | grep -q "has_resume"; then
    print_result "GET /api/status" "PASS"
else
    print_result "GET /api/status" "FAIL"
fi

# Test 2: Create test resume file
echo ""
echo "3️⃣  Testing Resume Upload..."
echo "Creating test resume..."
cat > /tmp/test_resume.txt << 'EOF'
John Doe
Software Engineer
Email: john.doe@example.com
Phone: (555) 123-4567

PROFESSIONAL SUMMARY
Experienced Full Stack Developer with 5+ years of expertise in building scalable web applications.

SKILLS
- Programming Languages: Python, JavaScript, TypeScript
- Frontend: React, Vue.js, HTML5, CSS3, Tailwind CSS
- Backend: Flask, Django, Node.js, Express
- Databases: PostgreSQL, MongoDB, MySQL, Redis
- DevOps: Docker, Kubernetes, AWS, CI/CD, Git
- Tools: VS Code, Postman, Jira, Slack

EXPERIENCE
Senior Software Engineer | Tech Corp | 2020-Present
- Developed microservices using Python and Flask
- Built responsive frontends with React and Tailwind
- Implemented CI/CD pipelines with Docker and Kubernetes
- Led team of 4 developers in agile environment

Software Developer | StartupXYZ | 2018-2020
- Created REST APIs with Django
- Developed single-page applications with Vue.js
- Managed PostgreSQL databases
- Collaborated with cross-functional teams

EDUCATION
Bachelor of Science in Computer Science
University of Technology | 2018

CERTIFICATIONS
- AWS Certified Developer Associate
- Docker Certified Associate
EOF

# Test 3: Upload Resume
response=$(curl -s -X POST -F "file=@/tmp/test_resume.txt" "$BASE_URL/api/upload-resume")
if echo "$response" | grep -q "Resume uploaded successfully"; then
    print_result "POST /api/upload-resume" "PASS"
else
    print_result "POST /api/upload-resume" "FAIL"
    echo "Response: $response"
fi

# Test 4: Check status after resume upload
response=$(curl -s "$BASE_URL/api/status")
if echo "$response" | grep -q '"has_resume": true'; then
    print_result "Resume upload verified" "PASS"
else
    print_result "Resume upload verified" "FAIL"
fi

echo ""
echo "4️⃣  Testing Job Management..."

# Test 5: Add Job
response=$(curl -s -X POST "$BASE_URL/api/jobs" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Full Stack Developer",
    "company": "Tech Corp",
    "description": "We are looking for an experienced Full Stack Developer with expertise in Python, React, Docker, and AWS. The ideal candidate will have experience with Flask, PostgreSQL, and CI/CD pipelines. Must be comfortable with microservices architecture and agile methodologies.",
    "url": "https://example.com/jobs/1",
    "status": "saved"
  }')

if echo "$response" | grep -q '"title": "Full Stack Developer"'; then
    print_result "POST /api/jobs (Add Job)" "PASS"
    JOB_ID=$(echo "$response" | grep -o '"id": [0-9]*' | head -1 | grep -o '[0-9]*')
    echo "  Created job with ID: $JOB_ID"
else
    print_result "POST /api/jobs (Add Job)" "FAIL"
    echo "Response: $response"
    JOB_ID=1
fi

# Test 6: Get All Jobs
response=$(curl -s "$BASE_URL/api/jobs")
if echo "$response" | grep -q "Full Stack Developer"; then
    print_result "GET /api/jobs (List Jobs)" "PASS"
else
    print_result "GET /api/jobs (List Jobs)" "FAIL"
fi

# Test 7: Get Specific Job
response=$(curl -s "$BASE_URL/api/jobs/$JOB_ID")
if echo "$response" | grep -q "Full Stack Developer"; then
    print_result "GET /api/jobs/$JOB_ID (Get Job)" "PASS"
else
    print_result "GET /api/jobs/$JOB_ID (Get Job)" "FAIL"
fi

# Test 8: Check Match Score
response=$(curl -s "$BASE_URL/api/jobs/$JOB_ID")
match_score=$(echo "$response" | grep -o '"match_score": [0-9.]*' | grep -o '[0-9.]*')
if [ ! -z "$match_score" ]; then
    print_result "Match score calculated" "PASS"
    echo "  Match Score: $match_score"
else
    print_result "Match score calculated" "FAIL"
fi

echo ""
echo "5️⃣  Testing Match Analysis..."

# Test 9: Get Match Details
response=$(curl -s "$BASE_URL/api/match/$JOB_ID")
if echo "$response" | grep -q "match_score"; then
    print_result "GET /api/match/$JOB_ID (Match Details)" "PASS"
else
    print_result "GET /api/match/$JOB_ID (Match Details)" "FAIL"
fi

# Test 10: Check Keyword Gaps
response=$(curl -s "$BASE_URL/api/jobs/$JOB_ID")
if echo "$response" | grep -q "keyword_gaps"; then
    print_result "Keyword gap analysis working" "PASS"
else
    print_result "Keyword gap analysis working" "FAIL"
fi

echo ""
echo "6️⃣  Testing Job Updates..."

# Test 11: Update Job Status
response=$(curl -s -X PUT "$BASE_URL/api/jobs/$JOB_ID" \
  -H "Content-Type: application/json" \
  -d '{"status": "applied"}')
if echo "$response" | grep -q '"status": "applied"'; then
    print_result "PUT /api/jobs/$JOB_ID (Update Status)" "PASS"
else
    print_result "PUT /api/jobs/$JOB_ID (Update Status)" "FAIL"
fi

# Test 12: Verify Update
response=$(curl -s "$BASE_URL/api/jobs/$JOB_ID")
if echo "$response" | grep -q '"status": "applied"'; then
    print_result "Status update verified" "PASS"
else
    print_result "Status update verified" "FAIL"
fi

echo ""
echo "7️⃣  Testing Additional Jobs..."

# Test 13: Add Another Job (Different Match)
response=$(curl -s -X POST "$BASE_URL/api/jobs" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Data Scientist",
    "company": "AI Labs",
    "description": "Looking for Data Scientist with Python, TensorFlow, Machine Learning, Deep Learning, and PyTorch experience.",
    "url": "https://example.com/jobs/2",
    "status": "saved"
  }')

if echo "$response" | grep -q '"title": "Data Scientist"'; then
    print_result "Add second job with different skills" "PASS"
    JOB_ID_2=$(echo "$response" | grep -o '"id": [0-9]*' | head -1 | grep -o '[0-9]*')
else
    print_result "Add second job with different skills" "FAIL"
fi

# Test 14: Verify Multiple Jobs
response=$(curl -s "$BASE_URL/api/jobs")
job_count=$(echo "$response" | grep -o '"id"' | wc -l)
if [ "$job_count" -ge 2 ]; then
    print_result "Multiple jobs stored" "PASS"
    echo "  Total jobs: $job_count"
else
    print_result "Multiple jobs stored" "FAIL"
fi

echo ""
echo "8️⃣  Testing Delete Functionality..."

# Test 15: Delete Job
if [ ! -z "$JOB_ID_2" ]; then
    response=$(curl -s -X DELETE "$BASE_URL/api/jobs/$JOB_ID_2")
    if echo "$response" | grep -q "deleted successfully"; then
        print_result "DELETE /api/jobs/$JOB_ID_2 (Delete Job)" "PASS"
    else
        print_result "DELETE /api/jobs/$JOB_ID_2 (Delete Job)" "FAIL"
    fi
else
    print_result "DELETE /api/jobs (Delete Job)" "SKIP"
fi

# Test 16: Verify Deletion
if [ ! -z "$JOB_ID_2" ]; then
    response=$(curl -s "$BASE_URL/api/jobs/$JOB_ID_2")
    if echo "$response" | grep -q "not found"; then
        print_result "Job deletion verified" "PASS"
    else
        print_result "Job deletion verified" "FAIL"
    fi
fi

echo ""
echo "9️⃣  Testing Error Handling..."

# Test 17: Invalid File Upload
response=$(curl -s -X POST "$BASE_URL/api/upload-resume")
if echo "$response" | grep -q "error"; then
    print_result "Error handling for missing file" "PASS"
else
    print_result "Error handling for missing file" "FAIL"
fi

# Test 18: Invalid Job Creation
response=$(curl -s -X POST "$BASE_URL/api/jobs" \
  -H "Content-Type: application/json" \
  -d '{}')
if echo "$response" | grep -q "error"; then
    print_result "Error handling for invalid job" "PASS"
else
    print_result "Error handling for invalid job" "FAIL"
fi

# Test 19: Non-existent Job
response=$(curl -s "$BASE_URL/api/jobs/99999")
if echo "$response" | grep -q "not found"; then
    print_result "Error handling for non-existent job" "PASS"
else
    print_result "Error handling for non-existent job" "FAIL"
fi

# Cleanup
rm -f /tmp/test_resume.txt

# Print summary
echo ""
echo "=============================================="
echo "📊 Test Summary"
echo "=============================================="
echo "Tests Run:    $TESTS_RUN"
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed! Application is working correctly.${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Test the frontend UI manually at http://localhost:3000"
    echo "  2. Run 'docker-compose up' to test Docker deployment"
    echo "  3. Review TESTING.md for comprehensive manual testing"
    exit 0
else
    echo -e "${RED}❌ Some tests failed. Please review the errors above.${NC}"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Check backend logs for errors"
    echo "  2. Verify all dependencies installed"
    echo "  3. Ensure NLTK data downloaded"
    echo "  4. Review TESTING.md for detailed guidance"
    exit 1
fi

