from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from src.models.user import db, User

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/register", methods=["POST"]) # Optional: Add user registration if needed
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"message": "Username, email, and password are required"}), 400

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"message": "Username or email already exists"}), 409

    try:
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        # Set is_admin based on some logic if needed, e.g., first user is admin
        # if User.query.count() == 0:
        #     new_user.is_admin = True
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully", "user_id": new_user.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        login_user(user) # Creates the session
        return jsonify({"message": "Login successful", "user": user.to_dict()}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

@auth_bp.route("/logout", methods=["POST"])
@login_required # User must be logged in to log out
def logout():
    logout_user() # Clears the session
    return jsonify({"message": "Logout successful"}), 200

@auth_bp.route("/status", methods=["GET"])
@login_required
def status():
    # Route to check if user is logged in and get their info
    return jsonify({"logged_in": True, "user": current_user.to_dict()}), 200

# Add a simple unauthorized handler for API requests
@auth_bp.app_errorhandler(401) # Or use login_manager.unauthorized
def unauthorized(error):
    # Check if the request expects JSON
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return jsonify(message="Unauthorized: Please log in."), 401
    # Handle non-API unauthorized access if needed (e.g., redirect to login page)
    # return redirect(url_for("auth_bp.login"))
    return jsonify(message="Unauthorized: Please log in."), 401 # Default to JSON response

