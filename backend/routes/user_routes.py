from flask import Blueprint, request, jsonify
from models.user import User, db
from auth.decorators import admin_required, same_user_or_admin_required

user_bp = Blueprint('users', __name__, url_prefix='/api/users')

@user_bp.route('/', methods=['GET'])
@admin_required
def get_users():
    """Get all users (admin only)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        team_id = request.args.get('team_id', type=int)
        role = request.args.get('role')
        is_active = request.args.get('is_active')
        
        query = User.query
        
        if team_id:
            query = query.filter_by(team_id=team_id)
        if role:
            query = query.filter_by(role=role)
        if is_active is not None:
            is_active_bool = is_active.lower() == 'true'
            query = query.filter_by(is_active=is_active_bool)
        
        users = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'users': [user.to_dict() for user in users.items],
            'pagination': {
                'page': users.page,
                'pages': users.pages,
                'per_page': users.per_page,
                'total': users.total,
                'has_next': users.has_next,
                'has_prev': users.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Error fetching users', 'error': str(e)}), 500

@user_bp.route('/<int:user_id>', methods=['GET'])
@same_user_or_admin_required
def get_user(user_id):
    """Get specific user"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'message': 'Error fetching user', 'error': str(e)}), 500

@user_bp.route('/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    """Update user (admin only)"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'role' in data:
            user.role = data['role']
        if 'team_id' in data:
            user.team_id = data['team_id']
        if 'is_active' in data:
            user.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'message': 'User updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating user', 'error': str(e)}), 500

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """Delete user (admin only)"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        # Soft delete - just deactivate
        user.is_active = False
        db.session.commit()
        
        return jsonify({'message': 'User deactivated successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error deactivating user', 'error': str(e)}), 500

@user_bp.route('/<int:user_id>/reactivate', methods=['PUT'])
@admin_required
def reactivate_user(user_id):
    """Reactivate user (admin only)"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        user.is_active = True
        db.session.commit()
        
        return jsonify({
            'message': 'User reactivated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error reactivating user', 'error': str(e)}), 500

@user_bp.route('/profile', methods=['GET'])
def get_profile():
    """Get current user's profile"""
    from flask_jwt_extended import jwt_required, get_jwt_identity
    
    try:
        jwt_required()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'message': 'Authentication required'}), 401

@user_bp.route('/profile', methods=['PUT'])
def update_profile():
    """Update current user's profile"""
    from flask_jwt_extended import jwt_required, get_jwt_identity
    
    try:
        jwt_required()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        data = request.get_json()
        
        # Users can only update their own name
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating profile', 'error': str(e)}), 500 