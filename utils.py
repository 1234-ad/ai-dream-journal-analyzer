"""
Utility functions for the AI Dream Journal Analyzer
"""
import re
import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataValidator:
    """Validates and sanitizes user input data"""
    
    @staticmethod
    def validate_dream_text(text: str) -> Tuple[bool, str]:
        """Validate dream text input"""
        if not text or not text.strip():
            return False, "Dream text cannot be empty"
        
        if len(text.strip()) < 10:
            return False, "Dream description too short (minimum 10 characters)"
        
        if len(text) > 5000:
            return False, "Dream description too long (maximum 5000 characters)"
        
        # Check for potentially harmful content
        harmful_patterns = [
            r'<script.*?>.*?</script>',
            r'javascript:',
            r'on\w+\s*=',
        ]
        
        for pattern in harmful_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return False, "Invalid characters detected"
        
        return True, "Valid"
    
    @staticmethod
    def validate_sleep_quality(quality: int) -> Tuple[bool, str]:
        """Validate sleep quality rating"""
        if not isinstance(quality, int):
            return False, "Sleep quality must be a number"
        
        if quality < 1 or quality > 10:
            return False, "Sleep quality must be between 1 and 10"
        
        return True, "Valid"
    
    @staticmethod
    def validate_date(date_obj) -> Tuple[bool, str]:
        """Validate dream date"""
        try:
            if date_obj > datetime.now().date():
                return False, "Dream date cannot be in the future"
            
            # Check if date is too far in the past (more than 10 years)
            if (datetime.now().date() - date_obj).days > 3650:
                return False, "Dream date too far in the past"
            
            return True, "Valid"
        except Exception as e:
            return False, f"Invalid date format: {str(e)}"

class DataProcessor:
    """Processes and cleans dream data"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize dream text"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;:\-\'"()]', '', text)
        
        return text
    
    @staticmethod
    def extract_keywords(text: str, min_length: int = 3) -> List[str]:
        """Extract meaningful keywords from dream text"""
        # Common stop words to exclude
        stop_words = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before',
            'after', 'above', 'below', 'between', 'among', 'throughout', 'despite',
            'towards', 'upon', 'concerning', 'was', 'were', 'been', 'have', 'has',
            'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may',
            'might', 'must', 'can', 'shall', 'this', 'that', 'these', 'those'
        }
        
        # Extract words
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        
        # Filter words
        keywords = [
            word for word in words 
            if len(word) >= min_length and word not in stop_words
        ]
        
        return list(set(keywords))  # Remove duplicates

class ErrorHandler:
    """Centralized error handling"""
    
    @staticmethod
    def handle_analysis_error(error: Exception, context: str = "") -> Dict:
        """Handle errors during dream analysis"""
        logger.error(f"Analysis error in {context}: {str(error)}")
        
        return {
            'success': False,
            'error': f"Analysis failed: {str(error)}",
            'fallback_data': {
                'polarity': 0.0,
                'subjectivity': 0.5,
                'emotion': 'neutral',
                'themes': [],
                'confidence': 0.0
            }
        }
    
    @staticmethod
    def handle_data_error(error: Exception, operation: str = "") -> Dict:
        """Handle data processing errors"""
        logger.error(f"Data error in {operation}: {str(error)}")
        
        return {
            'success': False,
            'error': f"Data processing failed: {str(error)}",
            'suggestion': "Please check your input and try again"
        }

class AdvancedAnalyzer:
    """Enhanced analysis capabilities"""
    
    def __init__(self):
        self.emotion_intensifiers = {
            'very': 1.5, 'extremely': 2.0, 'incredibly': 1.8,
            'really': 1.3, 'quite': 1.2, 'somewhat': 0.8,
            'slightly': 0.6, 'barely': 0.4
        }
        
        self.dream_symbols = {
            'water': ['ocean', 'river', 'lake', 'rain', 'flood', 'swimming'],
            'flying': ['fly', 'soar', 'wings', 'floating', 'levitate'],
            'animals': ['dog', 'cat', 'bird', 'snake', 'lion', 'bear', 'wolf'],
            'people': ['friend', 'family', 'stranger', 'crowd', 'person'],
            'places': ['house', 'school', 'work', 'city', 'forest', 'mountain'],
            'emotions': ['happy', 'sad', 'angry', 'scared', 'excited', 'worried']
        }
    
    def analyze_dream_complexity(self, text: str) -> Dict:
        """Analyze the complexity and richness of a dream"""
        words = text.split()
        sentences = text.split('.')
        
        # Calculate various metrics
        word_count = len(words)
        sentence_count = len([s for s in sentences if s.strip()])
        avg_sentence_length = word_count / max(sentence_count, 1)
        
        # Unique word ratio
        unique_words = len(set(word.lower() for word in words))
        uniqueness_ratio = unique_words / max(word_count, 1)
        
        # Symbol density
        symbol_count = 0
        for category, symbols in self.dream_symbols.items():
            for symbol in symbols:
                if symbol in text.lower():
                    symbol_count += 1
        
        symbol_density = symbol_count / max(word_count, 1) * 100
        
        # Complexity score (0-100)
        complexity_score = min(100, (
            (word_count / 10) * 0.3 +
            (uniqueness_ratio * 100) * 0.3 +
            symbol_density * 0.4
        ))
        
        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_sentence_length': round(avg_sentence_length, 1),
            'uniqueness_ratio': round(uniqueness_ratio, 2),
            'symbol_density': round(symbol_density, 1),
            'complexity_score': round(complexity_score, 1)
        }
    
    def detect_lucidity_indicators(self, text: str) -> Dict:
        """Detect potential lucidity indicators in dream text"""
        lucidity_keywords = [
            'realized', 'aware', 'conscious', 'control', 'lucid',
            'knew i was dreaming', 'reality check', 'dream sign'
        ]
        
        text_lower = text.lower()
        indicators_found = []
        
        for keyword in lucidity_keywords:
            if keyword in text_lower:
                indicators_found.append(keyword)
        
        lucidity_probability = min(1.0, len(indicators_found) * 0.3)
        
        return {
            'indicators': indicators_found,
            'probability': round(lucidity_probability, 2),
            'likely_lucid': lucidity_probability > 0.5
        }

def export_dreams_advanced(dreams_data: List[Dict], format_type: str = 'json') -> str:
    """Export dreams with advanced formatting options"""
    try:
        if format_type.lower() == 'json':
            return json.dumps(dreams_data, indent=2, default=str)
        
        elif format_type.lower() == 'csv':
            df = pd.DataFrame(dreams_data)
            return df.to_csv(index=False)
        
        elif format_type.lower() == 'markdown':
            markdown_content = "# Dream Journal Export\n\n"
            
            for i, dream in enumerate(dreams_data, 1):
                markdown_content += f"## Dream {i} - {dream.get('date', 'Unknown Date')}\n\n"
                markdown_content += f"**Text:** {dream.get('text', 'No description')}\n\n"
                markdown_content += f"**Emotion:** {dream.get('emotion', 'Unknown')}\n\n"
                markdown_content += f"**Themes:** {', '.join(dream.get('themes', []))}\n\n"
                markdown_content += f"**Sleep Quality:** {dream.get('sleep_quality', 'N/A')}/10\n\n"
                markdown_content += "---\n\n"
            
            return markdown_content
        
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    except Exception as e:
        logger.error(f"Export error: {str(e)}")
        return f"Export failed: {str(e)}"

def calculate_dream_statistics(dreams_data: List[Dict]) -> Dict:
    """Calculate comprehensive statistics from dream data"""
    if not dreams_data:
        return {}
    
    df = pd.DataFrame(dreams_data)
    
    stats = {
        'total_dreams': len(df),
        'date_range': {
            'earliest': df['date'].min() if 'date' in df.columns else None,
            'latest': df['date'].max() if 'date' in df.columns else None
        },
        'sentiment_stats': {
            'mean_polarity': df['polarity'].mean() if 'polarity' in df.columns else 0,
            'std_polarity': df['polarity'].std() if 'polarity' in df.columns else 0,
            'positive_dreams': len(df[df['polarity'] > 0.1]) if 'polarity' in df.columns else 0,
            'negative_dreams': len(df[df['polarity'] < -0.1]) if 'polarity' in df.columns else 0
        },
        'sleep_quality_stats': {
            'mean_quality': df['sleep_quality'].mean() if 'sleep_quality' in df.columns else 0,
            'best_night': df['sleep_quality'].max() if 'sleep_quality' in df.columns else 0,
            'worst_night': df['sleep_quality'].min() if 'sleep_quality' in df.columns else 0
        },
        'lucid_dream_stats': {
            'total_lucid': df['lucid'].sum() if 'lucid' in df.columns else 0,
            'lucid_percentage': (df['lucid'].sum() / len(df)) * 100 if 'lucid' in df.columns else 0
        }
    }
    
    return stats