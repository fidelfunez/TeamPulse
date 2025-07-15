from datetime import datetime
from sqlalchemy.orm import relationship

from .user import db

# Association table for many-to-many relationship between projects and users
project_assignments = db.Table('project_assignments',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('assigned_at', db.DateTime, default=datetime.utcnow, nullable=False)
)

class Project(db.Model):
    """Project model for tracking work and team assignments"""
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='active', nullable=False)  # 'active', 'completed', 'on_hold', 'cancelled'
    priority = db.Column(db.String(20), default='medium', nullable=False)  # 'low', 'medium', 'high', 'urgent'
    start_date = db.Column(db.Date, nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    team = relationship('Team', back_populates='projects')
    
    # Many-to-many relationship with users
    assigned_users = relationship('User', secondary=project_assignments, back_populates='assigned_projects')
    
    # Project check-ins (aggregated from team members)
    checkins = relationship('CheckIn', back_populates='project', cascade='all, delete-orphan')
    
    def __init__(self, title, team_id, description=None, status='active', priority='medium', 
                 start_date=None, due_date=None):
        self.title = title
        self.team_id = team_id
        self.description = description
        self.status = status
        self.priority = priority
        self.start_date = start_date
        self.due_date = due_date
    
    def to_dict(self):
        """Convert project to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'team_id': self.team_id,
            'team_name': self.team.name if self.team else None,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'assigned_users_count': len(self.assigned_users),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_with_users(self):
        """Convert project to dictionary with assigned user details"""
        project_dict = self.to_dict()
        project_dict['assigned_users'] = [user.to_dict() for user in self.assigned_users]
        return project_dict
    
    def is_overdue(self):
        """Check if project is overdue"""
        if self.due_date and self.status == 'active':
            from datetime import date
            return date.today() > self.due_date
        return False
    
    def __repr__(self):
        return f'<Project {self.title}>' 