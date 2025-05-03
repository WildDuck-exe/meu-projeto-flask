import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify, request # Added jsonify, request for error handler
from flask_login import LoginManager, login_required, current_user # Import login_required, current_user
from flask_cors import CORS

from src.models.user import db, User # Import User model

# Import Blueprints
from src.routes.user import user_bp
from src.routes.evento_api import evento_bp
from src.routes.noticia_api import noticia_bp
from src.routes.auth_api import auth_bp
from src.routes.inscricao_api import inscricao_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8000"}}) # Adiciona suporte a CORS
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT' # Change this in production!

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME', 'app_user')}:{os.getenv('DB_PASSWORD', 'ian148635')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'mydb')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Flask-Login Configuration
login_manager = LoginManager()
login_manager.init_app(app)
# If using session-based auth with separate frontend/backend, configure session cookie settings (e.g., SameSite, Secure)
# login_manager.login_view = 'auth_bp.login' # Specify the login view endpoint if using HTML forms

@login_manager.user_loader
def load_user(user_id):
    # Since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

# Custom Unauthorized handler for API
@login_manager.unauthorized_handler
def unauthorized():
    # Check if the request expects JSON
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return jsonify(message="Unauthorized: Please log in."), 401
    # Handle non-API unauthorized access if needed (e.g., redirect to login page)
    # return redirect(url_for('auth_bp.login'))
    return jsonify(message="Unauthorized: Please log in."), 401 # Default to JSON response

# Register Blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(evento_bp, url_prefix='/api')
app.register_blueprint(noticia_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(inscricao_bp, url_prefix='/api')

# Import models here to ensure they are known to SQLAlchemy before create_all
from src.models.evento import Evento
from src.models.noticia import Noticia
from src.models.inscricao import Inscricao

with app.app_context():
    db.create_all() # Creates tables based on models

# Serve Static Files (React/Vue build or simple HTML)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        # Serve specific file if it exists
        return send_from_directory(static_folder_path, path)
    else:
        # Serve index.html for SPA routing or if path is empty
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            # Only show 404 if index.html itself is missing
            return "index.html not found", 404

if __name__ == '__main__':
    # Use 0.0.0.0 to be accessible externally
    app.run(host='0.0.0.0', port=5000, debug=True) # debug=True for development only