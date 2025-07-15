from flask import Blueprint, request, jsonify
from models.checkin import CheckIn, db
from models.user import User
from models.project import Project
from auth.decorators import admin_required, employee_required, same_user_or_admin_required
from datetime import datetime, date, timedelta

checkin_bp = Blueprint('checkins', __name__, url_prefix='/api/checkins')

@checkin_bp.route('/', methods=['GET'])
@admin_required
def get_checkins():
    """Get all check-ins (admin only)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        user_id = request.args.get('user_id', type=int)
        team_id = request.args.get('team_id', type=int)
        project_id = request.args.get('project_id', type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = CheckIn.query
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        if project_id:
            query = query.filter_by(project_id=project_id)
        if team_id:
            query = query.join(User).filter(User.team_id == team_id)
        if start_date:
            query = query.filter(CheckIn.check_in_date >= start_date)
        if end_date:
            query = query.filter(CheckIn.check_in_date <= end_date)
        
        checkins = query.order_by(CheckIn.check_in_date.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'checkins': [checkin.to_dict() for checkin in checkins.items],
            'pagination': {
                'page': checkins.page,
                'pages': checkins.pages,
                'per_page': checkins.per_page,
                'total': checkins.total,
                'has_next': checkins.has_next,
                'has_prev': checkins.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Error fetching check-ins', 'error': str(e)}), 500

@checkin_bp.route('/my-checkins', methods=['GET'])
def get_my_checkins():
    """Get current user's check-ins"""
    try:
        from flask_jwt_extended import jwt_required, get_jwt_identity
        
        jwt_required()
        user_id = get_jwt_identity()
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = CheckIn.query.filter_by(user_id=user_id)
        
        if start_date:
            query = query.filter(CheckIn.check_in_date >= start_date)
        if end_date:
            query = query.filter(CheckIn.check_in_date <= end_date)
        
        checkins = query.order_by(CheckIn.check_in_date.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'checkins': [checkin.to_dict() for checkin in checkins.items],
            'pagination': {
                'page': checkins.page,
                'pages': checkins.pages,
                'per_page': checkins.per_page,
                'total': checkins.total,
                'has_next': checkins.has_next,
                'has_prev': checkins.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Error fetching check-ins', 'error': str(e)}), 500

@checkin_bp.route('/', methods=['POST'])
def create_checkin():
    """Create new check-in"""
    try:
        from flask_jwt_extended import jwt_required, get_jwt_identity
        
        jwt_required()
        user_id = get_jwt_identity()
        
        data = request.get_json()
        
        if not data.get('mood_rating'):
            return jsonify({'message': 'Mood rating is required'}), 400
        
        mood_rating = int(data['mood_rating'])
        if mood_rating < 1 or mood_rating > 5:
            return jsonify({'message': 'Mood rating must be between 1 and 5'}), 400
        
        # Check if user already has a check-in for today
        today = date.today()
        existing_checkin = CheckIn.query.filter_by(
            user_id=user_id, 
            check_in_date=today
        ).first()
        
        if existing_checkin:
            return jsonify({'message': 'You already have a check-in for today'}), 409
        
        checkin = CheckIn(
            user_id=user_id,
            mood_rating=mood_rating,
            project_id=data.get('project_id'),
            comment=data.get('comment'),
            work_load_rating=data.get('work_load_rating'),
            stress_level=data.get('stress_level'),
            check_in_date=today
        )
        
        db.session.add(checkin)
        db.session.commit()
        
        return jsonify({
            'message': 'Check-in submitted successfully',
            'checkin': checkin.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating check-in', 'error': str(e)}), 500

@checkin_bp.route('/<int:checkin_id>', methods=['GET'])
@same_user_or_admin_required
def get_checkin(checkin_id):
    """Get specific check-in"""
    try:
        checkin = CheckIn.query.get(checkin_id)
        
        if not checkin:
            return jsonify({'message': 'Check-in not found'}), 404
        
        return jsonify({'checkin': checkin.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'message': 'Error fetching check-in', 'error': str(e)}), 500

@checkin_bp.route('/<int:checkin_id>', methods=['PUT'])
@same_user_or_admin_required
def update_checkin(checkin_id):
    """Update check-in (same user or admin)"""
    try:
        checkin = CheckIn.query.get(checkin_id)
        
        if not checkin:
            return jsonify({'message': 'Check-in not found'}), 404
        
        data = request.get_json()
        
        if 'mood_rating' in data:
            mood_rating = int(data['mood_rating'])
            if mood_rating < 1 or mood_rating > 5:
                return jsonify({'message': 'Mood rating must be between 1 and 5'}), 400
            checkin.mood_rating = mood_rating
        
        if 'comment' in data:
            checkin.comment = data['comment']
        
        if 'work_load_rating' in data:
            work_load = data['work_load_rating']
            if work_load is not None and (work_load < 1 or work_load > 5):
                return jsonify({'message': 'Work load rating must be between 1 and 5'}), 400
            checkin.work_load_rating = work_load
        
        if 'stress_level' in data:
            stress_level = data['stress_level']
            if stress_level is not None and (stress_level < 1 or stress_level > 5):
                return jsonify({'message': 'Stress level must be between 1 and 5'}), 400
            checkin.stress_level = stress_level
        
        if 'project_id' in data:
            checkin.project_id = data['project_id']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Check-in updated successfully',
            'checkin': checkin.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating check-in', 'error': str(e)}), 500

@checkin_bp.route('/<int:checkin_id>', methods=['DELETE'])
@admin_required
def delete_checkin(checkin_id):
    """Delete check-in (admin only)"""
    try:
        checkin = CheckIn.query.get(checkin_id)
        
        if not checkin:
            return jsonify({'message': 'Check-in not found'}), 404
        
        db.session.delete(checkin)
        db.session.commit()
        
        return jsonify({'message': 'Check-in deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error deleting check-in', 'error': str(e)}), 500

@checkin_bp.route('/weekly-summary', methods=['GET'])
@admin_required
def get_weekly_summary():
    """Get weekly check-in summary (admin only)"""
    try:
        team_id = request.args.get('team_id', type=int)
        project_id = request.args.get('project_id', type=int)
        
        # Get date range for current week
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        
        query = CheckIn.query.filter(
            CheckIn.check_in_date >= start_of_week,
            CheckIn.check_in_date <= end_of_week
        )
        
        if team_id:
            query = query.join(User).filter(User.team_id == team_id)
        if project_id:
            query = query.filter(CheckIn.project_id == project_id)
        
        checkins = query.all()
        
        if not checkins:
            return jsonify({
                'message': 'No check-ins found for this week',
                'summary': {
                    'total_checkins': 0,
                    'average_mood': 0,
                    'average_workload': 0,
                    'average_stress': 0,
                    'date_range': {
                        'start': start_of_week.isoformat(),
                        'end': end_of_week.isoformat()
                    }
                }
            }), 200
        
        # Calculate averages
        total_mood = sum(c.mood_rating for c in checkins)
        avg_mood = round(total_mood / len(checkins), 2)
        
        workload_ratings = [c.work_load_rating for c in checkins if c.work_load_rating]
        avg_workload = round(sum(workload_ratings) / len(workload_ratings), 2) if workload_ratings else 0
        
        stress_levels = [c.stress_level for c in checkins if c.stress_level]
        avg_stress = round(sum(stress_levels) / len(stress_levels), 2) if stress_levels else 0
        
        return jsonify({
            'summary': {
                'total_checkins': len(checkins),
                'average_mood': avg_mood,
                'average_workload': avg_workload,
                'average_stress': avg_stress,
                'date_range': {
                    'start': start_of_week.isoformat(),
                    'end': end_of_week.isoformat()
                }
            },
            'checkins': [checkin.to_dict() for checkin in checkins]
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Error fetching weekly summary', 'error': str(e)}), 500 