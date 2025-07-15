from flask import Blueprint, request, jsonify
from models.team import Team, db
from models.user import User
from auth.decorators import admin_required

team_bp = Blueprint('teams', __name__, url_prefix='/api/teams')

@team_bp.route('/', methods=['GET'])
@admin_required
def get_teams():
    """Get all teams (admin only)"""
    try:
        teams = Team.query.all()
        
        return jsonify({
            'teams': [team.to_dict() for team in teams]
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Error fetching teams', 'error': str(e)}), 500

@team_bp.route('/<int:team_id>', methods=['GET'])
@admin_required
def get_team(team_id):
    """Get specific team with members"""
    try:
        team = Team.query.get(team_id)
        
        if not team:
            return jsonify({'message': 'Team not found'}), 404
        
        return jsonify({
            'team': team.to_dict_with_members()
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Error fetching team', 'error': str(e)}), 500

@team_bp.route('/', methods=['POST'])
@admin_required
def create_team():
    """Create new team (admin only)"""
    try:
        data = request.get_json()
        
        if not data.get('name'):
            return jsonify({'message': 'Team name is required'}), 400
        
        # Check if team name already exists
        existing_team = Team.query.filter_by(name=data['name']).first()
        if existing_team:
            return jsonify({'message': 'Team with this name already exists'}), 409
        
        team = Team(
            name=data['name'],
            description=data.get('description')
        )
        
        db.session.add(team)
        db.session.commit()
        
        return jsonify({
            'message': 'Team created successfully',
            'team': team.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating team', 'error': str(e)}), 500

@team_bp.route('/<int:team_id>', methods=['PUT'])
@admin_required
def update_team(team_id):
    """Update team (admin only)"""
    try:
        team = Team.query.get(team_id)
        
        if not team:
            return jsonify({'message': 'Team not found'}), 404
        
        data = request.get_json()
        
        if 'name' in data:
            # Check if new name conflicts with existing team
            existing_team = Team.query.filter_by(name=data['name']).first()
            if existing_team and existing_team.id != team_id:
                return jsonify({'message': 'Team with this name already exists'}), 409
            team.name = data['name']
        
        if 'description' in data:
            team.description = data['description']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Team updated successfully',
            'team': team.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating team', 'error': str(e)}), 500

@team_bp.route('/<int:team_id>', methods=['DELETE'])
@admin_required
def delete_team(team_id):
    """Delete team (admin only)"""
    try:
        team = Team.query.get(team_id)
        
        if not team:
            return jsonify({'message': 'Team not found'}), 404
        
        # Check if team has members
        if team.members:
            return jsonify({'message': 'Cannot delete team with members. Remove all members first.'}), 400
        
        # Check if team has projects
        if team.projects:
            return jsonify({'message': 'Cannot delete team with projects. Remove all projects first.'}), 400
        
        db.session.delete(team)
        db.session.commit()
        
        return jsonify({'message': 'Team deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error deleting team', 'error': str(e)}), 500

@team_bp.route('/<int:team_id>/members', methods=['GET'])
@admin_required
def get_team_members(team_id):
    """Get team members (admin only)"""
    try:
        team = Team.query.get(team_id)
        
        if not team:
            return jsonify({'message': 'Team not found'}), 404
        
        return jsonify({
            'team': team.to_dict(),
            'members': [member.to_dict() for member in team.members]
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Error fetching team members', 'error': str(e)}), 500

@team_bp.route('/<int:team_id>/members/<int:user_id>', methods=['POST'])
@admin_required
def add_team_member(team_id, user_id):
    """Add user to team (admin only)"""
    try:
        team = Team.query.get(team_id)
        user = User.query.get(user_id)
        
        if not team:
            return jsonify({'message': 'Team not found'}), 404
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        if user.team_id == team_id:
            return jsonify({'message': 'User is already a member of this team'}), 400
        
        user.team_id = team_id
        db.session.commit()
        
        return jsonify({
            'message': 'User added to team successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error adding user to team', 'error': str(e)}), 500

@team_bp.route('/<int:team_id>/members/<int:user_id>', methods=['DELETE'])
@admin_required
def remove_team_member(team_id, user_id):
    """Remove user from team (admin only)"""
    try:
        team = Team.query.get(team_id)
        user = User.query.get(user_id)
        
        if not team:
            return jsonify({'message': 'Team not found'}), 404
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        if user.team_id != team_id:
            return jsonify({'message': 'User is not a member of this team'}), 400
        
        user.team_id = None
        db.session.commit()
        
        return jsonify({
            'message': 'User removed from team successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error removing user from team', 'error': str(e)}), 500 