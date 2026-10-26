# 🎯 Resume-Job Matcher

A smart, production-ready job application assistant that matches your resume with job descriptions, identifies skill gaps, and tracks your applications with a beautiful modern UI.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![React](https://img.shields.io/badge/react-18.2-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 📄 **Smart Resume Upload**: Drag-and-drop support for PDF, DOCX, and TXT formats
- 🎯 **Intelligent Matching**: TF-IDF based ranking with optional ML embeddings upgrade
- 🔍 **Keyword Gap Analysis**: Identifies missing skills and keywords from job descriptions
- 📊 **Visual Dashboard**: Beautiful, responsive UI with real-time match scores and statistics
- 🏷️ **Application Tracking**: Organize jobs by status (Saved, Applied, Interview, Offer, Rejected)
- 🤖 **ML Mode**: Optional semantic matching using sentence embeddings for better context understanding
- 🐳 **Docker Ready**: One-command deployment with Docker Compose
- 🚀 **Production Ready**: Environment configuration, error handling, and optimized build

## 🚀 Quick Start

> **👉 New to this project? Start with [START_HERE.md](START_HERE.md) for a guided testing walkthrough!**

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd resume-job-matcher

# Run the setup script
chmod +x setup.sh
./setup.sh

# Start development servers
# Terminal 1 - Backend:
source venv/bin/activate
python backend/app.py

# Terminal 2 - Frontend:
cd frontend
npm run dev
```

Then open http://localhost:3000 for development or http://localhost:5000 for integrated mode.

### Option 2: Docker (Production)

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access the application
open http://localhost:5000
```

### Option 3: Manual Setup

#### Backend Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Start backend server
python backend/app.py
```

#### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## 🎨 Screenshots & Features

### Dashboard View
- Real-time statistics showing total jobs, average match score, applications, and interviews
- Clean, modern interface with smooth transitions and animations

### Resume Upload
- Drag-and-drop file upload with visual feedback
- Instant resume processing and parsing
- Support for multiple file formats

### Job Management
- Add jobs with title, company, description, and URL
- Automatic match score calculation upon adding
- Visual match indicators (Great/Good/Fair match)
- Status tracking throughout application process

### Match Analysis
- Detailed match score breakdown with circular progress indicator
- List of missing keywords from job description
- Actionable recommendations based on match score
- Full job description view

## 🏗️ Project Structure

```
resume-job-matcher/
├── backend/
│   ├── app.py              # Flask API server with all endpoints
│   ├── matcher.py          # TF-IDF and ML matching algorithms
│   ├── models.py           # SQLite database models
│   └── utils.py            # Resume parsing utilities (PDF, DOCX, TXT)
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── ResumeUpload.jsx
│   │   │   ├── JobList.jsx
│   │   │   ├── JobCard.jsx
│   │   │   ├── AddJobModal.jsx
│   │   │   └── MatchDetailsModal.jsx
│   │   ├── App.jsx         # Main application component
│   │   ├── api.js          # API service layer
│   │   ├── main.jsx        # Application entry point
│   │   └── index.css       # Tailwind CSS styles
│   ├── index.html
│   ├── package.json
│   └── vite.config.js      # Vite configuration with proxy
├── data/                   # Database storage (created automatically)
├── Dockerfile              # Multi-stage Docker build
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
├── setup.sh               # Automated setup script
├── .env.example           # Environment variables template
└── README.md
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory (copy from `.env.example`):

```bash
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=1

# Database
DATABASE_PATH=jobs.db

# File Upload
MAX_CONTENT_LENGTH=16777216  # 16MB in bytes
UPLOAD_FOLDER=/tmp

# Optional: Enable ML Mode
USE_ML_MODE=false
```

### Enabling ML Mode

For better semantic matching, enable ML mode:

```bash
# Install ML dependencies
pip install sentence-transformers torch

# Set in .env file
USE_ML_MODE=true
```

Or toggle it from the UI settings panel (⚙️ icon).

## 🧪 Testing & Production Readiness

This application is **production-ready** with comprehensive testing:

- **[START_HERE.md](START_HERE.md)** - Quick 5-minute testing guide
- **[RUN_TESTS.md](RUN_TESTS.md)** - Fast reference for running tests
- **[TESTING.md](TESTING.md)** - Comprehensive testing documentation
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guide
- **`test_app.sh`** - Automated test suite (19 tests)

### Quick Test

```bash
# Start backend
source venv/bin/activate
python backend/app.py

# Run automated tests (in another terminal)
./test_app.sh
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/status` | Get system status and configuration |
| `POST` | `/api/upload-resume` | Upload and parse resume file |
| `GET` | `/api/jobs` | Get all jobs with match scores |
| `POST` | `/api/jobs` | Add new job |
| `GET` | `/api/jobs/<id>` | Get specific job details |
| `PUT` | `/api/jobs/<id>` | Update job (status, details) |
| `DELETE` | `/api/jobs/<id>` | Delete job |
| `GET` | `/api/match/<job_id>` | Get detailed match analysis |
| `POST` | `/api/switch-mode` | Toggle TF-IDF/ML mode |

## 🧠 How It Works

### Matching Algorithms

#### 1. TF-IDF Mode (Default)
- **Fast**: No ML model loading required
- **Accurate**: Uses term frequency-inverse document frequency
- **Lightweight**: Works on any machine
- **Interpretable**: Clear keyword-based matching

#### 2. ML Embeddings Mode (Optional)
- **Semantic**: Understands context and meaning
- **Advanced**: Uses sentence-transformers (all-MiniLM-L6-v2)
- **Better Context**: Catches similar concepts with different words
- **Size**: ~500MB model download

### Keyword Gap Analysis

The system identifies important keywords from job descriptions that are missing from your resume using:
- TF-IDF scoring to find important terms
- N-gram analysis (unigrams and bigrams)
- Stopword filtering (preserving tech terms)
- Ranked by relevance

## 🎯 Usage Guide

1. **Upload Your Resume**
   - Drag and drop or click to upload
   - Supported formats: PDF, DOCX, TXT
   - Resume is parsed and stored securely

2. **Add Job Postings**
   - Click "Add Job" button
   - Paste job title, company, and full description
   - Optional: Add job posting URL
   - Match score calculated automatically

3. **Review Matches**
   - Jobs sorted by match score (highest first)
   - Color-coded match indicators
   - View missing keywords at a glance

4. **Track Applications**
   - Update status: Saved → Applied → Interview → Offer
   - Filter and organize your pipeline
   - Monitor your progress

5. **Analyze Gaps**
   - Click "View Details" on any job
   - See comprehensive match analysis
   - Get keyword recommendations
   - Tailor your resume accordingly

## 🛠️ Tech Stack

### Backend
- **Python 3.8+**: Core language
- **Flask**: Web framework
- **scikit-learn**: TF-IDF implementation
- **NLTK**: Natural language processing
- **sentence-transformers**: Optional ML embeddings
- **SQLite**: Database storage
- **PyPDF2 & python-docx**: Document parsing

### Frontend
- **React 18**: UI framework
- **Vite**: Build tool and dev server
- **Tailwind CSS**: Styling framework
- **Lucide React**: Icon library
- **Axios**: HTTP client

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Orchestration
- **Multi-stage builds**: Optimized images

## 🤝 Contributing

Contributions are welcome! Here are some ideas:

- [ ] Add LinkedIn job import
- [ ] Email notifications for good matches
- [ ] Resume tailoring suggestions
- [ ] Export reports to PDF
- [ ] Multi-user support with authentication
- [ ] Browser extension for easy job import
- [ ] Integration with job boards (Indeed, LinkedIn, etc.)

## 📝 License

MIT License - feel free to use, modify, and distribute!

## 🙏 Acknowledgments

- Built with modern Python and React best practices
- ML model from Hugging Face sentence-transformers
- Icons from Lucide React

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub. Or message me on linkedin.

---

**Made with ❤️ for job seekers everywhere**

