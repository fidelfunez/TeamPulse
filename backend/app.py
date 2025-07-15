import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from config import config
from models.user import db, bcrypt
from auth.jwt_auth import jwt
from routes import auth_bp, user_bp, team_bp, project_bp, checkin_bp, analytics_bp

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Setup CORS
    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)
    
    # Initialize migrations
    Migrate(app, db)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(team_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(checkin_bp)
    app.register_blueprint(analytics_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'message': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'message': 'Internal server error'}), 500
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'message': 'Method not allowed'}), 405
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'TeamPulse API is running'
        }), 200
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def root():
        return jsonify({
            'message': 'TeamPulse API',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'users': '/api/users',
                'teams': '/api/teams',
                'projects': '/api/projects',
                'checkins': '/api/checkins',
                'analytics': '/api/analytics'
            }
        }), 200
    
    return app

def init_db():
    """Initialize database with sample data"""
    from models.user import User
    from models.team import Team
    from models.project import Project
    
    # Create admin user if none exists
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin = User(
            email='admin@teampulse.com',
            password='admin123',
            first_name='Admin',
            last_name='User',
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created: admin@teampulse.com / admin123")
    
    # Create sample team if none exists
    if not Team.query.first():
        team = Team(
            name='Development Team',
            description='Main development team for the company'
        )
        db.session.add(team)
        db.session.commit()
        print("Sample team created: Development Team")
    
    # Create sample employee if none exists
    employee = User.query.filter_by(role='employee').first()
    if not employee:
        employee = User(
            email='employee@teampulse.com',
            password='employee123',
            first_name='John',
            last_name='Doe',
            role='employee',
            team_id=1
        )
        db.session.add(employee)
        db.session.commit()
        print("Sample employee created: employee@teampulse.com / employee123")
    
    # Create sample project if none exists
    if not Project.query.first():
        project = Project(
            title='TeamPulse Development',
            team_id=1,
            description='Building the TeamPulse application',
            status='active',
            priority='high'
        )
        db.session.add(project)
        db.session.commit()
        print("Sample project created: TeamPulse Development")

if __name__ == '__main__':
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Initialize with sample data
        init_db()
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=app.config.get('DEBUG', False)
    ) 