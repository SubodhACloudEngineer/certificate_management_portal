"""
Configuration for Certificate Portal
"""
import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Flask settings
    DEBUG = False
    TESTING = False
    
    # Portal settings
    PORTAL_TITLE = "Certificate Lifecycle Management"
    COMPANY_NAME = "NTT DATA"
    
    # Mock data path
    MOCK_DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'mock_certificates.json')
    
    # Pagination
    ITEMS_PER_PAGE = 50
    
    # Alert thresholds (days)
    ALERT_CRITICAL = 7
    ALERT_WARNING = 30
    ALERT_ATTENTION = 60
    ALERT_INFO = 90


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}