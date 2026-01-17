"""
Flask API server for Resume-Job Matcher
"""
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from models import Database
from matcher import get_matcher, TFIDFMatcher, EmbeddingMatcher
from utils import parse_resume
import tempfile

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Configuration
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', tempfile.gettempdir())
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))

# Database path (use data directory in production)
DB_PATH = os.environ.get('DATABASE_PATH', 'jobs.db')
if os.path.exists('/app/data'):  # Docker environment
    DB_PATH = '/app/data/jobs.db'

# Initialize database and matcher
db = Database(DB_PATH)
current_matcher = TFIDFMatcher()
use_ml_mode = os.environ.get('USE_ML_MODE', 'false').lower() == 'true'

# Try to load ML mode if specified
if use_ml_mode:
    try:
        current_matcher = EmbeddingMatcher()
        if not current_matcher.model:
            print("⚠ ML mode requested but model failed to load. Falling back to TF-IDF.")
            current_matcher = TFIDFMatcher()
            use_ml_mode = False
    except Exception as e:
        print(f"⚠ Error initializing ML mode: {e}. Falling back to TF-IDF.")
        current_matcher = TFIDFMatcher()
        use_ml_mode = False


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Serve the frontend"""
    # Try to serve built frontend first
    try:
        if os.path.exists(os.path.join(app.static_folder, 'dist', 'index.html')):
            return send_from_directory(os.path.join(app.static_folder, 'dist'), 'index.html')
        elif os.path.exists(os.path.join(app.static_folder, 'index.html')):
            # Check if it's the source index.html (has <div id="root">)
            with open(os.path.join(app.static_folder, 'index.html'), 'r') as f:
                content = f.read()
                if '<div id="root">' in content:
                    # This is the unbuilt Vite template, show fallback
                    return send_from_directory(app.static_folder, 'index-fallback.html')
            return send_from_directory(app.static_folder, 'index.html')
        else:
            return send_from_directory(app.static_folder, 'index-fallback.html')
    except:
        # Fallback to nice setup page
        return send_from_directory(app.static_folder, 'index-fallback.html')


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current system status"""
    resume = db.get_resume()
    return jsonify({
        'has_resume': resume is not None,
        'resume_filename': resume['filename'] if resume else None,
        'ml_mode': use_ml_mode,
        'matcher_type': 'ML Embeddings' if use_ml_mode else 'TF-IDF'
    })


@app.route('/api/upload-resume', methods=['POST'])
def upload_resume():
    """Upload and parse resume"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload PDF, DOCX, or TXT'}), 400
    
    try:
        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Parse resume
        resume_text = parse_resume(filepath, filename)
        
        # Clean up temp file
        os.remove(filepath)
        
        # Save to database
        db.save_resume(resume_text, filename)
        
        # Update matcher with new resume
        global current_matcher
        current_matcher.set_resume(resume_text)
        
        # Recalculate all job match scores
        jobs = db.get_all_jobs()
        for job in jobs:
            score = current_matcher.calculate_match_score(job['description'])
            gaps = current_matcher.find_keyword_gaps(job['description'])
            db.update_job(job['id'], match_score=score, keyword_gaps=gaps)
        
        return jsonify({
            'message': 'Resume uploaded successfully',
            'filename': filename,
            'preview': resume_text[:200] + '...' if len(resume_text) > 200 else resume_text
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Get all jobs with match scores"""
    jobs = db.get_all_jobs()
    return jsonify(jobs)


@app.route('/api/jobs', methods=['POST'])
def add_job():
    """Add a new job"""
    data = request.get_json()
    
    if not data or 'title' not in data or 'description' not in data:
        return jsonify({'error': 'Title and description are required'}), 400
    
    try:
        # Add job to database
        job_id = db.add_job(
            title=data['title'],
            company=data.get('company', ''),
            description=data['description'],
            url=data.get('url', ''),
            status=data.get('status', 'saved')
        )
        
        # Calculate match score if resume exists
        resume = db.get_resume()
        if resume:
            score = current_matcher.calculate_match_score(data['description'])
            gaps = current_matcher.find_keyword_gaps(data['description'])
            db.update_job(job_id, match_score=score, keyword_gaps=gaps)
        
        # Get the created job
        job = db.get_job(job_id)
        
        return jsonify(job), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """Get a specific job"""
    job = db.get_job(job_id)
    
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(job)


@app.route('/api/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    """Update a job"""
    job = db.get_job(job_id)
    
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    data = request.get_json()
    
    try:
        # Update job
        update_data = {}
        for field in ['title', 'company', 'description', 'url', 'status']:
            if field in data:
                update_data[field] = data[field]
        
        db.update_job(job_id, **update_data)
        
        # Recalculate match score if description changed
        if 'description' in data and db.get_resume():
            score = current_matcher.calculate_match_score(data['description'])
            gaps = current_matcher.find_keyword_gaps(data['description'])
            db.update_job(job_id, match_score=score, keyword_gaps=gaps)
        
        # Get updated job
        updated_job = db.get_job(job_id)
        
        return jsonify(updated_job)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    """Delete a job"""
    job = db.get_job(job_id)
    
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    try:
        db.delete_job(job_id)
        return jsonify({'message': 'Job deleted successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/match/<int:job_id>', methods=['GET'])
def get_match_details(job_id):
    """Get detailed match analysis for a job"""
    job = db.get_job(job_id)
    
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    resume = db.get_resume()
    
    if not resume:
        return jsonify({'error': 'Please upload a resume first'}), 400
    
    return jsonify({
        'job_id': job_id,
        'title': job['title'],
        'company': job['company'],
        'match_score': job['match_score'],
        'keyword_gaps': job['keyword_gaps'],
        'status': job['status']
    })


@app.route('/api/switch-mode', methods=['POST'])
def switch_mode():
    """Switch between TF-IDF and ML mode"""
    global current_matcher, use_ml_mode
    
    data = request.get_json()
    use_ml = data.get('use_ml', False)
    
    try:
        # Create new matcher
        current_matcher = get_matcher(use_ml)
        use_ml_mode = use_ml
        
        # Set resume if exists
        resume = db.get_resume()
        if resume:
            current_matcher.set_resume(resume['content'])
            
            # Recalculate all job scores
            jobs = db.get_all_jobs()
            for job in jobs:
                score = current_matcher.calculate_match_score(job['description'])
                gaps = current_matcher.find_keyword_gaps(job['description'])
                db.update_job(job['id'], match_score=score, keyword_gaps=gaps)
        
        return jsonify({
            'message': f'Switched to {"ML" if use_ml else "TF-IDF"} mode',
            'ml_mode': use_ml_mode
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 50)
    print("Resume-Job Matcher Server")
    print("=" * 50)
    print(f"Mode: {'ML Embeddings' if use_ml_mode else 'TF-IDF'}")
    print("Open http://localhost:8000 in your browser")
    print("=" * 50)
    
    app.run(debug=True, port=8000, host='127.0.0.1')

