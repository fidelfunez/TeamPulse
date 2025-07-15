from flask import Blueprint, request, jsonify
from models.project import Project, db, project_assignments
from models.user import User
from models.team import Team
from auth.decorators import admin_required, employee_required
from datetime import datetime

project_bp = Blueprint('projects', __name__, url_prefix='/api/projects')

@project_bp.route('/', methods=['GET'])
@employee_required
def get_projects():
    """Get projects (filtered by user role)"""
    try:
        from flask_jwt_extended import get_jwt_identity
        from auth.decorators import admin_required
        
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        team_id = request.args.get('team_id', type=int)
        status = request.args.get('status')
        priority = request.args.get('priority')
        
        query = Project.query
        
        # Filter by team if specified
        if team_id:
            query = query.filter_by(team_id=team_id)
        
        # Filter by status
        if status:
            query = query.filter_by(status=status)
        
        # Filter by priority
        if priority:
            query = query.filter_by(priority=priority)
        
        # If user is not admin, only show projects they're assigned to
        if user and not user.is_admin():
            query = query.join(project_assignments).filter(project_assignments.c.user_id == user_id)
        
        projects = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'projects': [project.to_dict() for project in projects.items],
            'pagination': {
                'page': projects.page,
                'pages': projects.pages,
                'per_page': projects.per_page,
                'total': projects.total,
                'has_next': projects.has_next,
                'has_prev': projects.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Error fetching projects', 'error': str(e)}), 500

@project_bp.route('/<int:project_id>', methods=['GET'])
@employee_required
def get_project(project_id):
    """Get specific project"""
    try:
        project = Project.query.get(project_id)
        
        if not project:
            return jsonify({'message': 'Project not found'}), 404
        
        return jsonify({
            'project': project.to_dict_with_users()
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Error fetching project', 'error': str(e)}), 500

@project_bp.route('/', methods=['POST'])
@admin_required
def create_project():
    """Create new project (admin only)"""
    try:
        data = request.get_json()
        
        if not data.get('title') or not data.get('team_id'):
            return jsonify({'message': 'Title and team_id are required'}), 400
        
        # Verify team exists
        team = Team.query.get(data['team_id'])
        if not team:
            return jsonify({'message': 'Team not found'}), 404
        
        project = Project(
            title=data['title'],
            team_id=data['team_id'],
            description=data.get('description'),
            status=data.get('status', 'active'),
            priority=data.get('priority', 'medium'),
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date() if data.get('start_date') else None,
            due_date=datetime.strptime(data['due_date'], '%Y-%m-%d').date() if data.get('due_date') else None
        )
        
        db.session.add(project)
        db.session.commit()
        
        return jsonify({
            'message': 'Project created successfully',
            'project': project.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating project', 'error': str(e)}), 500

@project_bp.route('/<int:project_id>', methods=['PUT'])
@admin_required
def update_project(project_id):
    """Update project (admin only)"""
    try:
        project = Project.query.get(project_id)
        
        if not project:
            return jsonify({'message': 'Project not found'}), 404
        
        data = request.get_json()
        
        if 'title' in data:
            project.title = data['title']
        if 'description' in data:
            project.description = data['description']
        if 'status' in data:
            project.status = data['status']
        if 'priority' in data:
            project.priority = data['priority']
        if 'team_id' in data:
            # Verify team exists
            team = Team.query.get(data['team_id'])
            if not team:
                return jsonify({'message': 'Team not found'}), 404
            project.team_id = data['team_id']
        if 'start_date' in data:
            project.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date() if data['start_date'] else None
        if 'due_date' in data:
            project.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date() if data['due_date'] else None
        
        db.session.commit()
        
        return jsonify({
            'message': 'Project updated successfully',
            'project': project.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating project', 'error': str(e)}), 500

@project_bp.route('/<int:project_id>', methods=['DELETE'])
@admin_required
def delete_project(project_id):
    """Delete project (admin only)"""
    try:
        project = Project.query.get(project_id)
        
        if not project:
            return jsonify({'message': 'Project not found'}), 404
        
        db.session.delete(project)
        db.session.commit()
        
        return jsonify({'message': 'Project deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error deleting project', 'error': str(e)}), 500

@project_bp.route('/<int:project_id>/assign/<int:user_id>', methods=['POST'])
@admin_required
def assign_user_to_project(project_id, user_id):
    """Assign user to project (admin only)"""
    try:
        project = Project.query.get(project_id)
        user = User.query.get(user_id)
        
        if not project:
            return jsonify({'message': 'Project not found'}), 404
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        if user in project.assigned_users:
            return jsonify({'message': 'User is already assigned to this project'}), 400
        
        project.assigned_users.append(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User assigned to project successfully',
            'project': project.to_dict_with_users()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error assigning user to project', 'error': str(e)}), 500

@project_bp.route('/<int:project_id>/unassign/<int:user_id>', methods=['DELETE'])
@admin_required
def unassign_user_from_project(project_id, user_id):
    """Unassign user from project (admin only)"""
    try:
        project = Project.query.get(project_id)
        user = User.query.get(user_id)
        
        if not project:
            return jsonify({'message': 'Project not found'}), 404
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        if user not in project.assigned_users:
            return jsonify({'message': 'User is not assigned to this project'}), 400
        
        project.assigned_users.remove(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User unassigned from project successfully',
            'project': project.to_dict_with_users()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error unassigning user from project', 'error': str(e)}), 500

@project_bp.route('/<int:project_id>/assigned-users', methods=['GET'])
@employee_required
def get_project_assigned_users(project_id):
    """Get users assigned to project"""
    try:
        project = Project.query.get(project_id)
        
        if not project:
            return jsonify({'message': 'Project not found'}), 404
        
        return jsonify({
            'project': project.to_dict(),
            'assigned_users': [user.to_dict() for user in project.assigned_users]
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Error fetching project users', 'error': str(e)}), 500 