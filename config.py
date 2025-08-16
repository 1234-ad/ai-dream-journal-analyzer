"""
Configuration settings for AI Dream Journal Analyzer
"""
import os
from typing import Dict, List

class Config:
    """Application configuration"""
    
    # App settings
    APP_NAME = "AI Dream Journal Analyzer"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "AI-powered dream journal with pattern analysis and predictions"
    
    # UI settings
    PAGE_TITLE = "🌙 AI Dream Journal Analyzer"
    PAGE_ICON = "🌙"
    LAYOUT = "wide"
    INITIAL_SIDEBAR_STATE = "expanded"
    
    # Analysis settings
    MIN_DREAM_LENGTH = 10
    MAX_DREAM_LENGTH = 5000
    MIN_DREAMS_FOR_PREDICTION = 3
    
    # Theme detection keywords
    DREAM_THEMES = {
        'flying': [
            'fly', 'flying', 'soar', 'soaring', 'wings', 'air', 'sky', 
            'floating', 'levitate', 'hovering', 'glide', 'gliding'
        ],
        'falling': [
            'fall', 'falling', 'drop', 'dropping', 'cliff', 'height', 
            'plummet', 'tumble', 'tumbling', 'descent'
        ],
        'chase': [
            'chase', 'chasing', 'run', 'running', 'escape', 'escaping',
            'pursue', 'pursuing', 'follow', 'following', 'hunt', 'hunting'
        ],
        'water': [
            'water', 'ocean', 'sea', 'river', 'lake', 'swim', 'swimming',
            'drown', 'drowning', 'flood', 'flooding', 'rain', 'storm'
        ],
        'animals': [
            'dog', 'cat', 'bird', 'snake', 'lion', 'tiger', 'bear',
            'wolf', 'horse', 'elephant', 'animal', 'pet', 'wild'
        ],
        'death': [
            'death', 'die', 'dying', 'dead', 'funeral', 'grave',
            'cemetery', 'corpse', 'ghost', 'spirit'
        ],
        'school': [
            'school', 'teacher', 'exam', 'test', 'classroom', 'student',
            'homework', 'grade', 'university', 'college'
        ],
        'work': [
            'work', 'office', 'boss', 'meeting', 'job', 'career',
            'colleague', 'workplace', 'business', 'professional'
        ],
        'family': [
            'mother', 'father', 'mom', 'dad', 'family', 'parent',
            'sibling', 'brother', 'sister', 'child', 'relative'
        ],
        'house': [
            'house', 'home', 'room', 'bedroom', 'kitchen', 'bathroom',
            'door', 'window', 'stairs', 'basement', 'attic'
        ],
        'vehicle': [
            'car', 'truck', 'bus', 'train', 'plane', 'airplane',
            'boat', 'ship', 'bicycle', 'motorcycle', 'vehicle'
        ],
        'food': [
            'food', 'eat', 'eating', 'meal', 'dinner', 'lunch',
            'breakfast', 'restaurant', 'kitchen', 'cooking'
        ]
    }
    
    # Emotion detection keywords
    EMOTION_KEYWORDS = {
        'joy': [
            'happy', 'joy', 'joyful', 'excited', 'wonderful', 'amazing',
            'great', 'fantastic', 'love', 'loving', 'bliss', 'euphoric',
            'delighted', 'cheerful', 'elated', 'thrilled'
        ],
        'fear': [
            'scared', 'afraid', 'terrified', 'nightmare', 'horror',
            'panic', 'frightened', 'anxious', 'worried', 'nervous',
            'dread', 'terror', 'phobia', 'fearful'
        ],
        'anger': [
            'angry', 'mad', 'furious', 'rage', 'annoyed', 'frustrated',
            'irritated', 'upset', 'hostile', 'aggressive', 'violent',
            'outraged', 'livid', 'enraged'
        ],
        'sadness': [
            'sad', 'depressed', 'crying', 'tears', 'lonely', 'grief',
            'sorrow', 'melancholy', 'miserable', 'heartbroken',
            'devastated', 'mourning', 'despair'
        ],
        'anxiety': [
            'worried', 'anxious', 'nervous', 'stress', 'stressed',
            'tension', 'uneasy', 'restless', 'agitated', 'troubled',
            'concerned', 'apprehensive'
        ],
        'love': [
            'love', 'loving', 'romantic', 'romance', 'affection',
            'tender', 'caring', 'passionate', 'intimate', 'adore',
            'cherish', 'devotion'
        ],
        'surprise': [
            'surprised', 'shock', 'shocked', 'amazed', 'astonished',
            'stunned', 'bewildered', 'confused', 'unexpected',
            'sudden', 'startled'
        ]
    }
    
    # Lucidity indicators
    LUCIDITY_KEYWORDS = [
        'realized', 'aware', 'conscious', 'control', 'lucid',
        'knew i was dreaming', 'reality check', 'dream sign',
        'became aware', 'took control', 'dream control',
        'lucid dreaming', 'wake up in dream'
    ]
    
    # Color scheme
    COLORS = {
        'primary': '#4A90E2',
        'secondary': '#764ba2',
        'success': '#28a745',
        'warning': '#ffc107',
        'danger': '#dc3545',
        'info': '#17a2b8',
        'light': '#f8f9fa',
        'dark': '#343a40'
    }
    
    # Chart settings
    CHART_CONFIG = {
        'height': 400,
        'theme': 'plotly_white',
        'color_palette': [
            '#4A90E2', '#764ba2', '#FF6B6B', '#4ECDC4',
            '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD'
        ]
    }
    
    # Export settings
    EXPORT_FORMATS = ['json', 'csv', 'markdown']
    MAX_EXPORT_SIZE = 10000  # Maximum number of dreams to export
    
    # Validation rules
    VALIDATION_RULES = {
        'min_word_count': 3,
        'max_word_count': 1000,
        'min_sleep_quality': 1,
        'max_sleep_quality': 10,
        'max_date_past_days': 3650,  # 10 years
    }
    
    # Feature flags
    FEATURES = {
        'advanced_analytics': True,
        'dream_predictions': True,
        'export_functionality': True,
        'lucidity_detection': True,
        'theme_analysis': True,
        'sentiment_analysis': True,
        'pattern_recognition': True
    }
    
    # API settings (for future integrations)
    API_SETTINGS = {
        'rate_limit': 100,  # requests per minute
        'timeout': 30,  # seconds
        'retry_attempts': 3
    }
    
    @classmethod
    def get_theme_keywords(cls, theme: str) -> List[str]:
        """Get keywords for a specific theme"""
        return cls.DREAM_THEMES.get(theme, [])
    
    @classmethod
    def get_emotion_keywords(cls, emotion: str) -> List[str]:
        """Get keywords for a specific emotion"""
        return cls.EMOTION_KEYWORDS.get(emotion, [])
    
    @classmethod
    def is_feature_enabled(cls, feature: str) -> bool:
        """Check if a feature is enabled"""
        return cls.FEATURES.get(feature, False)
    
    @classmethod
    def get_color(cls, color_name: str) -> str:
        """Get color by name"""
        return cls.COLORS.get(color_name, '#000000')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    LOG_LEVEL = 'INFO'

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    LOG_LEVEL = 'DEBUG'
    
    # Reduced limits for testing
    MIN_DREAM_LENGTH = 5
    MAX_DREAM_LENGTH = 1000
    MIN_DREAMS_FOR_PREDICTION = 2

# Configuration factory
def get_config(env: str = None) -> Config:
    """Get configuration based on environment"""
    env = env or os.getenv('ENVIRONMENT', 'development').lower()
    
    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }
    
    return config_map.get(env, DevelopmentConfig)()