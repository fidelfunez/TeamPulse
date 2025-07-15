from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from models.user import User

def admin_required(fn):
    """Decorator to require admin role"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.is_admin():
            return jsonify({'message': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

def employee_required(fn):
    """Decorator to require employee role (or admin)"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.is_active:
            return jsonify({'message': 'Valid user access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

def same_user_or_admin_required(fn):
    """Decorator to require same user or admin access"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.is_active:
            return jsonify({'message': 'Valid user access required'}), 403
        
        # Admin can access any user's data
        if current_user.is_admin():
            return fn(*args, **kwargs)
        
        # Check if user is accessing their own data
        target_user_id = kwargs.get('user_id') or request.args.get('user_id')
        if target_user_id and int(target_user_id) != current_user_id:
            return jsonify({'message': 'Access denied'}), 403
        
        return fn(*args, **kwargs)
    return wrapper 