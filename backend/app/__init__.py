# app/__init__.py
import os
from flask import Flask
from .config import config_by_name
from .extensions import db, migrate, jwt, cors

# Add these imports for logging
import logging
from logging.handlers import RotatingFileHandler

def create_app(config_name='dev'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Ensure the instance folder exists for SQLite
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite:///'):
        # Assuming 'instance' is at the same level as the 'app' directory,
        # so one level up from app.root_path which is '.../ai_research_assistant/app'
        instance_path = os.path.join(os.path.dirname(app.root_path), 'instance')
        if not os.path.exists(instance_path):
            try:
                os.makedirs(instance_path)
                # app.logger.info(f"Created instance folder at {instance_path}") # Logger not configured yet here
                print(f"Created instance folder at {instance_path}")
            except OSError as e:
                print(f"Error creating instance folder at {instance_path}: {e}")

    # Ensure paper save directory exists
    paper_save_dir = app.config['PAPER_SAVE_DIR']
    if not os.path.exists(paper_save_dir):
        try:
            os.makedirs(paper_save_dir, exist_ok=True)
            print(f"Paper save directory created/ensured at: {paper_save_dir}")
        except OSError as e:
            print(f"Error creating paper save directory at {paper_save_dir}: {e}")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    # cors.init_app(app, resources={r"/api/*": {"origins": "*"}}) # Adjust origins for production
    cors.init_app(app, supports_credentials=True, origins="*")

    # --- Logging Configuration ---
    if True: #not app.debug and not app.testing: # Only enable file logging when not in debug or testing
        # Define log directory (one level up from app.root_path, then into 'logs')
        log_dir = os.path.join(os.path.dirname(app.root_path), 'logs')
        if not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
            except OSError as e:
                # Fallback or raise error if log directory cannot be created
                print(f"Error creating log directory {log_dir}: {e}")
                # You might want to handle this more gracefully or ensure it's created by deployment scripts

        # Log file path
        log_file = os.path.join(log_dir, 'app.log')

        # Rotating File Handler
        # Max 10MB per file, keep last 5 backup files
        file_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024 * 10, backupCount=5, encoding='utf-8')
        
        # Log Formatter
        # Example format: 2023-10-27 10:30:00,123 INFO in module:message (lineno)
        log_formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        file_handler.setFormatter(log_formatter)
        
        # Set Log Level for the file handler
        # You can get this from app.config if you want to make it configurable
        file_handler.setLevel(logging.INFO) # Or logging.WARNING, logging.ERROR

        # Add the file handler to the Flask app's logger
        # app.logger is a standard Python logger, so you can add handlers to it.
        # If you want to log Werkzeug requests as well, you might need to configure the root logger
        # or Werkzeug's specific logger, but app.logger handles app-specific logs.
        
        # Clear existing handlers if any (e.g., default StreamHandler)
        # if you want *only* file logging and not console output in production.
        # Be careful with this if other extensions add handlers.
        # app.logger.handlers.clear() # Optional: if you want ONLY file logging

        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO) # Set overall app logger level
        
        # Log that the logger itself is configured
        app.logger.info('Application logging to file configured.')
    else:
        # For debug or testing, Flask's default console logger is usually fine.
        # You can customize it further if needed.
        app.logger.setLevel(logging.DEBUG) # Ensure debug level for console in dev
        app.logger.info('Application running in DEBUG mode, logging to console.')


    # Register Blueprints
    from .api.auth import auth_bp
    from .api.papers import papers_bp
    from .api.rag import rag_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(papers_bp, url_prefix='/api/papers')
    app.register_blueprint(rag_bp, url_prefix='/api/rag')

    # Shell context for flask cli
    @app.shell_context_processor
    def ctx():
        from app.models.user import User
        from app.models.paper import PaperMetadata
        from app.models.chat import ChatMessage, ChatSession
        return {
            'app': app, 'db': db, 
            'User': User, 'PaperMetadata': PaperMetadata, 
            'ChatMessage': ChatMessage, 'ChatSession': ChatSession
        }

    return app