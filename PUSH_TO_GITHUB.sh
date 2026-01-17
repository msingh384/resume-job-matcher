#!/bin/bash

# Resume-Job Matcher - Push to GitHub Script
# This script will help you push your project to GitHub

echo "╔═══════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                           ║"
echo "║          🚀 PUSH RESUME-JOB MATCHER TO GITHUB 🚀                         ║"
echo "║                                                                           ║"
echo "╚═══════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first:"
    echo "   brew install git"
    exit 1
fi

echo "✅ Git is installed"
echo ""

# Navigate to project directory
cd /Users/mannanrajsingh/resume-job-matcher

# Initialize git if not already done
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already initialized"
fi
echo ""

# Configure git user if not set (optional)
if [ -z "$(git config user.name)" ]; then
    echo "⚙️  Git user not configured. Please set your name and email:"
    read -p "Enter your name: " git_name
    read -p "Enter your email: " git_email
    git config user.name "$git_name"
    git config user.email "$git_email"
    echo "✅ Git user configured"
    echo ""
fi

# Add all files
echo "📝 Adding files to git..."
git add .
echo "✅ Files added"
echo ""

# Show status
echo "📊 Git status:"
git status --short
echo ""

# Commit
echo "💾 Creating commit..."
git commit -m "Initial commit: Production-ready Resume-Job Matcher

- Backend API with Flask (Python)
- Frontend UI with React and Vite
- TF-IDF matching algorithm with optional ML mode
- Resume parsing (PDF, DOCX, TXT)
- Job management and tracking
- Docker containerization
- Comprehensive testing suite (19 automated tests)
- Complete documentation
- All tests passing ✅"

echo "✅ Commit created"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌐 NEXT STEPS: Create GitHub Repository"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Go to: https://github.com/new"
echo ""
echo "2. Create a new repository:"
echo "   - Repository name: resume-job-matcher"
echo "   - Description: Smart job application assistant with resume matching"
echo "   - Public or Private: Your choice"
echo "   - ⚠️  Do NOT initialize with README, .gitignore, or license"
echo ""
echo "3. After creating the repository, copy the repository URL"
echo "   (It will look like: https://github.com/YOUR_USERNAME/resume-job-matcher.git)"
echo ""
echo "4. Then run these commands:"
echo ""
echo "   git remote add origin YOUR_REPO_URL"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "Press Enter after you've created the GitHub repository..."
echo ""
read -p "Enter your GitHub repository URL: " repo_url

if [ -z "$repo_url" ]; then
    echo "❌ No URL provided. Please run the commands manually:"
    echo ""
    echo "   git remote add origin YOUR_REPO_URL"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    exit 1
fi

# Add remote
echo ""
echo "🔗 Adding remote repository..."
git remote add origin "$repo_url" 2>/dev/null || git remote set-url origin "$repo_url"
echo "✅ Remote added"
echo ""

# Rename branch to main
echo "📝 Renaming branch to main..."
git branch -M main
echo "✅ Branch renamed"
echo ""

# Push to GitHub
echo "🚀 Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                           ║"
    echo "║          🎉 SUCCESS! PROJECT PUSHED TO GITHUB! 🎉                        ║"
    echo "║                                                                           ║"
    echo "╚═══════════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "✅ Your project is now on GitHub!"
    echo ""
    echo "📝 Next steps:"
    echo "   1. View your repository in browser"
    echo "   2. Add a repository description on GitHub"
    echo "   3. Add topics/tags: python, flask, react, job-search, resume-matcher"
    echo "   4. Star your own repo! ⭐"
    echo ""
else
    echo ""
    echo "❌ Push failed. You may need to authenticate with GitHub."
    echo ""
    echo "If you need to authenticate:"
    echo "   - Use GitHub CLI: gh auth login"
    echo "   - Or use SSH: Generate SSH key and add to GitHub"
    echo "   - Or use Personal Access Token"
    echo ""
fi

