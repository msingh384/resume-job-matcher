# 🚀 Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- Node.js 16+ and npm (for frontend development)
- Docker (optional, for containerized deployment)

## Method 1: Docker (Easiest)

```bash
# Build and run
docker-compose up --build

# Open in browser
open http://localhost:5000
```

Done! 🎉

## Method 2: Development Mode

### Step 1: Backend Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download required NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Start backend
python backend/app.py
```

Backend running at http://localhost:5000 ✅

### Step 2: Frontend Setup (in new terminal)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend running at http://localhost:3000 ✅

## First Steps

1. **Upload Your Resume**
   - Open the app in your browser
   - Drag and drop your resume (PDF, DOCX, or TXT)
   - Wait for processing (usually < 5 seconds)

2. **Add Your First Job**
   - Click "Add Job" button
   - Fill in job title and paste the description
   - Click "Add Job"
   - Watch the match score calculate automatically!

3. **Explore**
   - View detailed match analysis
   - Check missing keywords
   - Update application status
   - Add more jobs

## Optional: Enable ML Mode

For better semantic matching:

```bash
# Install ML dependencies
pip install sentence-transformers torch

# In the app, click Settings (⚙️) and toggle ML Mode
```

Note: First time will download ~500MB model.

## Troubleshooting

### Backend won't start
- Check Python version: `python3 --version` (need 3.8+)
- Ensure NLTK data downloaded
- Check if port 5000 is available

### Frontend won't start
- Check Node version: `node --version` (need 16+)
- Try removing `node_modules` and run `npm install` again
- Check if port 3000 is available

### Resume upload fails
- Check file size (max 16MB)
- Ensure file is PDF, DOCX, or TXT
- Try a different file

### Docker build fails
- Ensure Docker is running
- Try: `docker-compose down && docker-compose up --build`

## Next Steps

- Read the [full README](README.md) for detailed documentation
- Check [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Explore the API endpoints in the README

## Need Help?

Open an issue on GitHub with:
- What you tried
- Error messages
- Your environment (OS, Python version, etc.)

Happy job hunting! 🎯

