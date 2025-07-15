from datetime import datetime, date
from sqlalchemy.orm import relationship

from .user import db

class CheckIn(db.Model):
    """CheckIn model for tracking employee morale and weekly updates"""
    __tablename__ = 'checkins'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)
    check_in_date = db.Column(db.Date, nullable=False, default=date.today)
    mood_rating = db.Column(db.Integer, nullable=False)  # 1-5 scale
    comment = db.Column(db.Text, nullable=True)
    work_load_rating = db.Column(db.Integer, nullable=True)  # 1-5 scale
    stress_level = db.Column(db.Integer, nullable=True)  # 1-5 scale
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship('User', back_populates='checkins')
    project = relationship('Project', back_populates='checkins')
    
    def __init__(self, user_id, mood_rating, project_id=None, comment=None, 
                 work_load_rating=None, stress_level=None, check_in_date=None):
        self.user_id = user_id
        self.mood_rating = mood_rating
        self.project_id = project_id
        self.comment = comment
        self.work_load_rating = work_load_rating
        self.stress_level = stress_level
        self.check_in_date = check_in_date or date.today()
    
    def to_dict(self):
        """Convert check-in to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': f"{self.user.first_name} {self.user.last_name}" if self.user else None,
            'project_id': self.project_id,
            'project_title': self.project.title if self.project else None,
            'check_in_date': self.check_in_date.isoformat() if self.check_in_date else None,
            'mood_rating': self.mood_rating,
            'comment': self.comment,
            'work_load_rating': self.work_load_rating,
            'stress_level': self.stress_level,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def get_mood_description(self):
        """Get human-readable mood description"""
        mood_descriptions = {
            1: "Very Low",
            2: "Low", 
            3: "Neutral",
            4: "Good",
            5: "Excellent"
        }
        return mood_descriptions.get(self.mood_rating, "Unknown")
    
    def get_workload_description(self):
        """Get human-readable workload description"""
        if not self.work_load_rating:
            return None
        workload_descriptions = {
            1: "Very Light",
            2: "Light",
            3: "Moderate", 
            4: "Heavy",
            5: "Very Heavy"
        }
        return workload_descriptions.get(self.work_load_rating, "Unknown")
    
    def get_stress_description(self):
        """Get human-readable stress level description"""
        if not self.stress_level:
            return None
        stress_descriptions = {
            1: "Very Low",
            2: "Low",
            3: "Moderate",
            4: "High", 
            5: "Very High"
        }
        return stress_descriptions.get(self.stress_level, "Unknown")
    
    @classmethod
    def get_weekly_average_mood(cls, team_id=None, project_id=None, start_date=None, end_date=None):
        """Get average mood rating for a period"""
        from .user import User
        query = cls.query
        
        if team_id:
            query = query.join(User).filter(User.team_id == team_id)
        if project_id:
            query = query.filter(cls.project_id == project_id)
        if start_date:
            query = query.filter(cls.check_in_date >= start_date)
        if end_date:
            query = query.filter(cls.check_in_date <= end_date)
        
        checkins = query.all()
        if not checkins:
            return 0
        
        total_mood = sum(checkin.mood_rating for checkin in checkins)
        return round(total_mood / len(checkins), 2)
    
    def __repr__(self):
        return f'<CheckIn {self.user_id} - {self.check_in_date} - Mood: {self.mood_rating}>' 