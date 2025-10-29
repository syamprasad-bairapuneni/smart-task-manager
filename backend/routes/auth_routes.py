from flask import Blueprint, request, jsonify
from models import db, User, UserRole
from utils.auth import generate_token, generate_refresh_token, verify_token, token_required

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Email and password are required'}), 400
        
        if not data.get('name'):
            return jsonify({'message': 'Name is required'}), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        name = data['name'].strip()
        role = UserRole.USER  # Default role
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'message': 'User with this email already exists'}), 400
        
        # Create new user
        user = User(
            name=name,
            email=email,
            role=role
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Generate tokens
        token = generate_token(user.id, user.email, user.role.value)
        refresh_token = generate_refresh_token(user.id)
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict(),
            'token': token,
            'refresh_token': refresh_token
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Registration failed: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Email and password are required'}), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return jsonify({'message': 'Invalid email or password'}), 401
        
        # Generate tokens
        token = generate_token(user.id, user.email, user.role.value)
        refresh_token = generate_refresh_token(user.id)
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'token': token,
            'refresh_token': refresh_token
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Login failed: {str(e)}'}), 500


@auth_bp.route('/refresh', methods=['POST'])
def refresh_token():
    """Refresh access token using refresh token"""
    try:
        data = request.get_json()
        
        if not data or not data.get('refresh_token'):
            return jsonify({'message': 'Refresh token is required'}), 400
        
        refresh_token = data['refresh_token']
        payload = verify_token(refresh_token)
        
        if not payload or payload.get('type') != 'refresh':
            return jsonify({'message': 'Invalid refresh token'}), 401
        
        # Get user
        user = User.query.get(payload['user_id'])
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        # Generate new tokens
        token = generate_token(user.id, user.email, user.role.value)
        new_refresh_token = generate_refresh_token(user.id)
        
        return jsonify({
            'token': token,
            'refresh_token': new_refresh_token
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Token refresh failed: {str(e)}'}), 500


@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user_id, **kwargs):
    """Get current user profile"""
    try:
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        return jsonify({
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Failed to get profile: {str(e)}'}), 500


@auth_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile(current_user_id, **kwargs):
    """Update current user profile"""
    try:
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        data = request.get_json()
        
        if data.get('name'):
            user.name = data['name'].strip()
        
        # Email update would require verification, skipping for now
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to update profile: {str(e)}'}), 500

