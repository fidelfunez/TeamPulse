from flask import jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from functools import wraps

jwt = JWTManager()

def create_user_token(user_id, email, role):
    """Create JWT access token with user info"""
    return create_access_token(
        identity=user_id,
        additional_claims={
            'email': email,
            'role': role
        }
    )

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """Handle expired token"""
    return jsonify({
        'message': 'The token has expired',
        'error': 'token_expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    """Handle invalid token"""
    return jsonify({
        'message': 'Signature verification failed',
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    """Handle missing token"""
    return jsonify({
        'message': 'Request does not contain an access token',
        'error': 'authorization_required'
    }), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    """Handle non-fresh token when fresh token required"""
    return jsonify({
        'message': 'The token is not fresh',
        'error': 'fresh_token_required'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    """Handle revoked token"""
    return jsonify({
        'message': 'The token has been revoked',
        'error': 'token_revoked'
    }), 401 