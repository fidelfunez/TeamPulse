from datetime import datetime
from sqlalchemy.orm import relationship

from .user import db

class Team(db.Model):
    """Team model for organizing users and projects"""
    __tablename__ = 'teams'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    members = relationship('User', back_populates='team', cascade='all, delete-orphan')
    projects = relationship('Project', back_populates='team', cascade='all, delete-orphan')
    
    def __init__(self, name, description=None):
        self.name = name
        self.description = description
    
    def to_dict(self):
        """Convert team to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'member_count': len(self.members),
            'project_count': len(self.projects),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_with_members(self):
        """Convert team to dictionary with member details"""
        team_dict = self.to_dict()
        team_dict['members'] = [member.to_dict() for member in self.members]
        return team_dict
    
    def __repr__(self):
        return f'<Team {self.name}>' 