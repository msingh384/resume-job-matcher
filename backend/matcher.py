"""
Job matching algorithms - TF-IDF and ML embeddings
"""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from typing import List, Dict, Tuple
import re


# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)


class JobMatcher:
    """Base class for job matching"""
    
    def __init__(self):
        self.resume_text = None
        self.stop_words = set(stopwords.words('english'))
        # Keep important tech-related words
        self.stop_words -= {'not', 'no', 'can', 'will', 'should'}
    
    def set_resume(self, resume_text: str):
        """Set the resume text for matching"""
        self.resume_text = self.preprocess_text(resume_text)
    
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess text"""
        # Convert to lowercase
        text = text.lower()
        # Remove URLs
        text = re.sub(r'http\S+|www.\S+', '', text)
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        # Keep alphanumeric, +, #, and -
        text = re.sub(r'[^\w\s\+\#\-]', ' ', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def calculate_match_score(self, job_description: str) -> float:
        """Calculate match score between resume and job description"""
        raise NotImplementedError("Subclasses must implement this method")
    
    def find_keyword_gaps(self, job_description: str, top_n: int = 10) -> List[str]:
        """Find keywords in job description that are missing from resume"""
        raise NotImplementedError("Subclasses must implement this method")


class TFIDFMatcher(JobMatcher):
    """TF-IDF based matching (fast, no ML required)"""
    
    def __init__(self):
        super().__init__()
        self.vectorizer = TfidfVectorizer(
            max_features=500,
            stop_words='english',
            ngram_range=(1, 2),  # Use unigrams and bigrams
            min_df=1
        )
    
    def calculate_match_score(self, job_description: str) -> float:
        """Calculate cosine similarity between resume and job description"""
        if not self.resume_text:
            return 0.0
        
        job_desc_processed = self.preprocess_text(job_description)
        
        try:
            # Fit and transform both texts
            tfidf_matrix = self.vectorizer.fit_transform([self.resume_text, job_desc_processed])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            # Convert to percentage (0-100)
            return round(similarity * 100, 2)
        except Exception as e:
            print(f"Error calculating match score: {e}")
            return 0.0
    
    def find_keyword_gaps(self, job_description: str, top_n: int = 10) -> List[str]:
        """Find important keywords from job that are missing in resume"""
        if not self.resume_text:
            return []
        
        job_desc_processed = self.preprocess_text(job_description)
        
        # Get tokens
        resume_tokens = set(word_tokenize(self.resume_text.lower()))
        job_tokens = word_tokenize(job_desc_processed.lower())
        
        # Get TF-IDF scores for job description
        try:
            tfidf_matrix = self.vectorizer.fit_transform([job_desc_processed])
            feature_names = self.vectorizer.get_feature_names_out()
            tfidf_scores = tfidf_matrix.toarray()[0]
            
            # Create word-score pairs
            word_scores = list(zip(feature_names, tfidf_scores))
            # Sort by score (descending)
            word_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Find missing keywords
            gaps = []
            for word, score in word_scores:
                # Check if word/phrase is in resume
                if word not in self.resume_text.lower():
                    # Also check if it's a meaningful word (not in stopwords)
                    tokens_in_phrase = word.split()
                    if not all(token in self.stop_words for token in tokens_in_phrase):
                        gaps.append(word)
                
                if len(gaps) >= top_n:
                    break
            
            return gaps
        except Exception as e:
            print(f"Error finding keyword gaps: {e}")
            return []


class EmbeddingMatcher(JobMatcher):
    """Embedding-based matching using sentence-transformers (ML upgrade)"""
    
    def __init__(self):
        super().__init__()
        self.model = None
        self.resume_embedding = None
        self._load_model()
    
    def _load_model(self):
        """Load the sentence transformer model"""
        try:
            from sentence_transformers import SentenceTransformer
            # Use a lightweight but effective model
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            print("✓ ML model loaded successfully")
        except ImportError:
            print("⚠ sentence-transformers not installed. Install with: pip install sentence-transformers")
            self.model = None
        except Exception as e:
            print(f"⚠ Error loading ML model: {e}")
            self.model = None
    
    def set_resume(self, resume_text: str):
        """Set resume and compute embedding"""
        super().set_resume(resume_text)
        if self.model and self.resume_text:
            self.resume_embedding = self.model.encode(self.resume_text, convert_to_tensor=False)
    
    def calculate_match_score(self, job_description: str) -> float:
        """Calculate semantic similarity using embeddings"""
        if not self.model or not self.resume_embedding is not None:
            print("⚠ ML model not available, falling back to TF-IDF")
            # Fallback to TF-IDF
            matcher = TFIDFMatcher()
            matcher.set_resume(self.resume_text if self.resume_text else "")
            return matcher.calculate_match_score(job_description)
        
        try:
            job_desc_processed = self.preprocess_text(job_description)
            job_embedding = self.model.encode(job_desc_processed, convert_to_tensor=False)
            
            # Calculate cosine similarity
            similarity = cosine_similarity(
                self.resume_embedding.reshape(1, -1),
                job_embedding.reshape(1, -1)
            )[0][0]
            
            # Convert to percentage
            return round(similarity * 100, 2)
        except Exception as e:
            print(f"Error calculating embedding match score: {e}")
            return 0.0
    
    def find_keyword_gaps(self, job_description: str, top_n: int = 10) -> List[str]:
        """Find keyword gaps (using TF-IDF for interpretability)"""
        # Even in ML mode, we use TF-IDF for keyword gaps because it's more interpretable
        matcher = TFIDFMatcher()
        matcher.set_resume(self.resume_text if self.resume_text else "")
        return matcher.find_keyword_gaps(job_description, top_n)


def get_matcher(use_ml: bool = False) -> JobMatcher:
    """Factory function to get the appropriate matcher"""
    if use_ml:
        return EmbeddingMatcher()
    else:
        return TFIDFMatcher()

