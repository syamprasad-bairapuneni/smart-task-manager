from flask import Flask
from flask_cors import CORS
from models import db
import os
from dotenv import load_dotenv
from sqlalchemy import text

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
# Support both MySQL and SQLite for easy setup
database_url = os.getenv('DATABASE_URL')
if not database_url:
    # Use SQLite as fallback for easy local development; ensure absolute path
    basedir = os.path.dirname(os.path.abspath(__file__))
    sqlite_path = os.path.join(basedir, 'task_manager.db')
    database_url = f'sqlite:///{sqlite_path}'
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_ORIGINS'] = os.getenv('CORS_ORIGINS', '*')

# Initialize extensions
db.init_app(app)
# Dev-friendly CORS: allow any origin if set to '*', otherwise use provided list
if app.config['CORS_ORIGINS'] == '*':
    CORS(app, resources={r"/api/*": {"origins": "*"}})
else:
    CORS(app, origins=app.config['CORS_ORIGINS'].split(','), supports_credentials=True)

# Import routes
from routes.auth_routes import auth_bp
from routes.task_routes import task_bp
from routes.analytics_routes import analytics_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(task_bp, url_prefix='/api/tasks')
app.register_blueprint(analytics_bp, url_prefix='/api/analytics')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return {'status': 'healthy', 'message': 'Task Manager API is running'}, 200


@app.route('/', methods=['GET'])
def root():
    """Friendly root message to help local testing"""
    return {
        'message': 'Smart Task & Productivity Manager API',
        'endpoints': {
            'health': '/api/health',
            'auth': '/api/auth/*',
            'tasks': '/api/tasks/*',
            'analytics': '/api/analytics/*'
        }
    }, 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # SQLite migration helper for dev: add completed_at if missing
        try:
            engine = db.engine
            if engine.name == 'sqlite':
                with engine.connect() as conn:
                    cols = conn.execute(text("PRAGMA table_info(tasks)")).fetchall()
                    col_names = {c[1] for c in cols}
                    if 'completed_at' not in col_names:
                        conn.execute(text('ALTER TABLE tasks ADD COLUMN completed_at DATETIME NULL'))
                        conn.commit()
        except Exception:
            pass
    app.run(debug=True, host='0.0.0.0', port=5000)

