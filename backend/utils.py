"""
Utilities for resume parsing and text processing
"""
import re
from typing import Optional
import PyPDF2
import docx


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    except Exception as e:
        raise Exception(f"Error reading DOCX: {str(e)}")


def extract_text_from_txt(file_path: str) -> str:
    """Extract text from TXT file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except Exception as e:
        raise Exception(f"Error reading TXT: {str(e)}")


def parse_resume(file_path: str, filename: str) -> str:
    """
    Parse resume file and extract text
    Supports PDF, DOCX, and TXT formats
    """
    file_extension = filename.lower().split('.')[-1]
    
    if file_extension == 'pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension == 'docx':
        return extract_text_from_docx(file_path)
    elif file_extension == 'txt':
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")


def clean_text(text: str) -> str:
    """Clean and normalize text"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep important ones
    text = re.sub(r'[^\w\s\+\#\-\.]', ' ', text)
    return text.strip()


def extract_keywords(text: str, top_n: int = 20) -> list:
    """
    Extract important keywords from text
    This is a simple implementation that looks for common tech skills
    """
    text_lower = text.lower()
    
    # Common tech keywords to look for
    tech_keywords = [
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go', 'rust', 'swift',
        'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring',
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'ci/cd',
        'sql', 'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch',
        'machine learning', 'deep learning', 'ai', 'nlp', 'computer vision',
        'agile', 'scrum', 'git', 'github', 'gitlab', 'rest api', 'graphql',
        'microservices', 'serverless', 'terraform', 'ansible',
        'html', 'css', 'sass', 'tailwind', 'bootstrap',
        'testing', 'unit testing', 'integration testing', 'tdd',
        'data structures', 'algorithms', 'system design', 'architecture'
    ]
    
    found_keywords = []
    for keyword in tech_keywords:
        if keyword in text_lower:
            found_keywords.append(keyword)
    
    return found_keywords[:top_n]

