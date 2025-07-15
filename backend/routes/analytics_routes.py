from flask import Blueprint, request, jsonify
from models.checkin import CheckIn
from models.user import User
from models.team import Team
from models.project import Project
from auth.decorators import admin_required
from datetime import datetime, date, timedelta
from sqlalchemy import func, and_

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')

@analytics_bp.route('/dashboard-basic', methods=['GET'])
def get_basic_dashboard_data():
    """Get basic dashboard stats (all authenticated users)"""
    try:
        from flask_jwt_extended import jwt_required, get_jwt_identity
        
        jwt_required()
        user_id = get_jwt_identity()
        
        # Get date range (default to last 30 days)
        days = request.args.get('days', 30, type=int)
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        # Total users
        total_users = User.query.filter_by(is_active=True).count()
        
        # Total teams
        total_teams = Team.query.count()
        
        # Total projects
        total_projects = Project.query.count()
        active_projects = Project.query.filter_by(status='active').count()
        
        # Check-in statistics
        checkins = CheckIn.query.filter(
            CheckIn.check_in_date >= start_date,
            CheckIn.check_in_date <= end_date
        ).all()
        
        total_checkins = len(checkins)
        
        # Recent check-ins (last 7 days)
        recent_start = end_date - timedelta(days=7)
        recent_checkins = CheckIn.query.filter(
            CheckIn.check_in_date >= recent_start,
            CheckIn.check_in_date <= end_date
        ).count()
        
        return jsonify({
            'overview': {
                'total_users': total_users,
                'total_teams': total_teams,
                'total_projects': total_projects,
                'active_projects': active_projects,
                'total_checkins': total_checkins,
                'recent_checkins': recent_checkins
            },
            'date_range': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat(),
                'days': days
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Error fetching dashboard data', 'error': str(e)}), 500

@analytics_bp.route('/dashboard', methods=['GET'])
@admin_required
def get_dashboard_data():
    """Get dashboard analytics (admin only)"""
    try:
        # Get date range (default to last 30 days)
        days = request.args.get('days', 30, type=int)
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        # Total users
        total_users = User.query.filter_by(is_active=True).count()
        
        # Total teams
        total_teams = Team.query.count()
        
        # Total projects
        total_projects = Project.query.count()
        active_projects = Project.query.filter_by(status='active').count()
        
        # Check-in statistics
        checkins = CheckIn.query.filter(
            CheckIn.check_in_date >= start_date,
            CheckIn.check_in_date <= end_date
        ).all()
        
        total_checkins = len(checkins)
        avg_mood = 0
        avg_workload = 0
        avg_stress = 0
        
        if checkins:
            total_mood = sum(c.mood_rating for c in checkins)
            avg_mood = round(total_mood / len(checkins), 2)
            
            workload_ratings = [c.work_load_rating for c in checkins if c.work_load_rating]
            if workload_ratings:
                avg_workload = round(sum(workload_ratings) / len(workload_ratings), 2)
            
            stress_levels = [c.stress_level for c in checkins if c.stress_level]
            if stress_levels:
                avg_stress = round(sum(stress_levels) / len(stress_levels), 2)
        
        # Recent check-ins (last 7 days)
        recent_start = end_date - timedelta(days=7)
        recent_checkins = CheckIn.query.filter(
            CheckIn.check_in_date >= recent_start,
            CheckIn.check_in_date <= end_date
        ).count()
        
        return jsonify({
            'overview': {
                'total_users': total_users,
                'total_teams': total_teams,
                'total_projects': total_projects,
                'active_projects': active_projects,
                'total_checkins': total_checkins,
                'recent_checkins': recent_checkins
            },
            'averages': {
                'mood': avg_mood,
                'workload': avg_workload,
                'stress': avg_stress
            },
            'date_range': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat(),
                'days': days
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Error fetching dashboard data', 'error': str(e)}), 500

@analytics_bp.route('/teams', methods=['GET'])
@admin_required
def get_team_analytics():
    """Get team analytics (admin only)"""
    try:
        days = request.args.get('days', 30, type=int)
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        teams = Team.query.all()
        team_data = []
        
        for team in teams:
            # Get team members
            members = User.query.filter_by(team_id=team.id, is_active=True).all()
            
            # Get team check-ins
            checkins = CheckIn.query.join(User).filter(
                User.team_id == team.id,
                CheckIn.check_in_date >= start_date,
                CheckIn.check_in_date <= end_date
            ).all()
            
            avg_mood = 0
            avg_workload = 0
            avg_stress = 0
            
            if checkins:
                total_mood = sum(c.mood_rating for c in checkins)
                avg_mood = round(total_mood / len(checkins), 2)
                
                workload_ratings = [c.work_load_rating for c in checkins if c.work_load_rating]
                if workload_ratings:
                    avg_workload = round(sum(workload_ratings) / len(workload_ratings), 2)
                
                stress_levels = [c.stress_level for c in checkins if c.stress_level]
                if stress_levels:
                    avg_stress = round(sum(stress_levels) / len(stress_levels), 2)
            
            team_data.append({
                'team': team.to_dict(),
                'member_count': len(members),
                'checkin_count': len(checkins),
                'averages': {
                    'mood': avg_mood,
                    'workload': avg_workload,
                    'stress': avg_stress
                }
            })
        
        return jsonify({
            'teams': team_data,
            'date_range': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat(),
                'days': days
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Error fetching team analytics', 'error': str(e)}), 500

@analytics_bp.route('/projects', methods=['GET'])
@admin_required
def get_project_analytics():
    """Get project analytics (admin only)"""
    try:
        days = request.args.get('days', 30, type=int)
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        projects = Project.query.all()
        project_data = []
        
        for project in projects:
            # Get project check-ins
            checkins = CheckIn.query.filter(
                CheckIn.project_id == project.id,
                CheckIn.check_in_date >= start_date,
                CheckIn.check_in_date <= end_date
            ).all()
            
            avg_mood = 0
            avg_workload = 0
            avg_stress = 0
            
            if checkins:
                total_mood = sum(c.mood_rating for c in checkins)
                avg_mood = round(total_mood / len(checkins), 2)
                
                workload_ratings = [c.work_load_rating for c in checkins if c.work_load_rating]
                if workload_ratings:
                    avg_workload = round(sum(workload_ratings) / len(workload_ratings), 2)
                
                stress_levels = [c.stress_level for c in checkins if c.stress_level]
                if stress_levels:
                    avg_stress = round(sum(stress_levels) / len(stress_levels), 2)
            
            project_data.append({
                'project': project.to_dict(),
                'assigned_users_count': len(project.assigned_users),
                'checkin_count': len(checkins),
                'averages': {
                    'mood': avg_mood,
                    'workload': avg_workload,
                    'stress': avg_stress
                }
            })
        
        return jsonify({
            'projects': project_data,
            'date_range': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat(),
                'days': days
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Error fetching project analytics', 'error': str(e)}), 500

@analytics_bp.route('/trends', methods=['GET'])
@admin_required
def get_trends():
    """Get mood trends over time (admin only)"""
    try:
        days = request.args.get('days', 30, type=int)
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        # Get daily averages
        daily_data = db.session.query(
            CheckIn.check_in_date,
            func.avg(CheckIn.mood_rating).label('avg_mood'),
            func.avg(CheckIn.work_load_rating).label('avg_workload'),
            func.avg(CheckIn.stress_level).label('avg_stress'),
            func.count(CheckIn.id).label('checkin_count')
        ).filter(
            CheckIn.check_in_date >= start_date,
            CheckIn.check_in_date <= end_date
        ).group_by(CheckIn.check_in_date).order_by(CheckIn.check_in_date).all()
        
        trends = []
        for day_data in daily_data:
            trends.append({
                'date': day_data.check_in_date.isoformat(),
                'avg_mood': float(day_data.avg_mood) if day_data.avg_mood else 0,
                'avg_workload': float(day_data.avg_workload) if day_data.avg_workload else 0,
                'avg_stress': float(day_data.avg_stress) if day_data.avg_stress else 0,
                'checkin_count': day_data.checkin_count
            })
        
        return jsonify({
            'trends': trends,
            'date_range': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat(),
                'days': days
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Error fetching trends', 'error': str(e)}), 500 