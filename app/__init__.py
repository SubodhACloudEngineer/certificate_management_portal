"""
Flask application factory
"""
from flask import Flask
from config import config

def create_app(config_name='default'):
    """Create and configure Flask application"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Register blueprints
    from app.routes.dashboard import dashboard_bp
    from app.routes.inventory import inventory_bp
    from app.routes.discovery import discovery_bp
    from app.routes.reports import reports_bp
    
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(discovery_bp, url_prefix='/discovery')
    app.register_blueprint(reports_bp, url_prefix='/reports')
    
    return app