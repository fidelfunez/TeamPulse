# TeamPulse Backend

Flask-based REST API for TeamPulse, providing authentication, user management, team management, project tracking, and analytics.

## Features

- **Authentication**: JWT-based authentication with role-based access control
- **User Management**: CRUD operations for users with team assignments
- **Team Management**: Create, update, and manage teams with member assignments
- **Project Management**: Track projects with user assignments and status
- **Check-in System**: Weekly employee check-ins with mood and workload tracking
- **Analytics**: Dashboard analytics, team insights, and trend analysis
- **Database**: PostgreSQL with SQLAlchemy ORM and migrations

## Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL
- pip

### Installation

1. **Clone and navigate to backend**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your settings
   ```

5. **Set up database**
   ```bash
   # Create PostgreSQL database
   createdb teampulse_db
   
   # Run the application (creates tables and sample data)
   python app.py
   ```

6. **Run the server**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## Environment Variables

Create a `.env` file in the backend directory:

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-change-this-in-production

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/teampulse_db

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production
JWT_ACCESS_TOKEN_EXPIRES=3600

# CORS Configuration
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

## Database Models

### User
- `id`: Primary key
- `email`: Unique email address
- `password_hash`: Bcrypt hashed password
- `first_name`, `last_name`: User names
- `role`: 'admin' or 'employee'
- `is_active`: Account status
- `team_id`: Foreign key to Team
- `created_at`, `updated_at`: Timestamps

### Team
- `id`: Primary key
- `name`: Team name (unique)
- `description`: Team description
- `created_at`, `updated_at`: Timestamps

### Project
- `id`: Primary key
- `title`: Project title
- `description`: Project description
- `status`: 'active', 'completed', 'on_hold', 'cancelled'
- `priority`: 'low', 'medium', 'high', 'urgent'
- `team_id`: Foreign key to Team
- `start_date`, `due_date`: Project dates
- `created_at`, `updated_at`: Timestamps

### CheckIn
- `id`: Primary key
- `user_id`: Foreign key to User
- `project_id`: Foreign key to Project (optional)
- `check_in_date`: Date of check-in
- `mood_rating`: 1-5 scale
- `comment`: Optional text comment
- `work_load_rating`: 1-5 scale (optional)
- `stress_level`: 1-5 scale (optional)
- `created_at`, `updated_at`: Timestamps

## API Endpoints

### Authentication

#### POST /api/auth/login
Login with email and password.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "access_token": "jwt_token_here",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "admin",
    "team_id": 1
  }
}
```

#### POST /api/auth/register
Register new user (admin only).

**Request:**
```json
{
  "email": "newuser@example.com",
  "password": "password123",
  "first_name": "Jane",
  "last_name": "Smith",
  "role": "employee",
  "team_id": 1
}
```

### Users

#### GET /api/users
Get all users (admin only).

**Query Parameters:**
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20)
- `team_id`: Filter by team
- `role`: Filter by role
- `is_active`: Filter by active status

#### GET /api/users/:id
Get specific user.

#### PUT /api/users/:id
Update user (admin only).

**Request:**
```json
{
  "first_name": "Updated Name",
  "role": "admin",
  "team_id": 2
}
```

### Teams

#### GET /api/teams
Get all teams (admin only).

#### POST /api/teams
Create new team (admin only).

**Request:**
```json
{
  "name": "New Team",
  "description": "Team description"
}
```

### Projects

#### GET /api/projects
Get projects (filtered by user role).

**Query Parameters:**
- `page`: Page number
- `per_page`: Items per page
- `team_id`: Filter by team
- `status`: Filter by status
- `priority`: Filter by priority

#### POST /api/projects
Create new project (admin only).

**Request:**
```json
{
  "title": "New Project",
  "team_id": 1,
  "description": "Project description",
  "status": "active",
  "priority": "high",
  "start_date": "2024-01-01",
  "due_date": "2024-12-31"
}
```

### Check-ins

#### GET /api/checkins/my-checkins
Get current user's check-ins.

#### POST /api/checkins
Create new check-in.

**Request:**
```json
{
  "mood_rating": 4,
  "project_id": 1,
  "comment": "Feeling good today!",
  "work_load_rating": 3,
  "stress_level": 2
}
```

#### GET /api/checkins/weekly-summary
Get weekly summary (admin only).

**Query Parameters:**
- `team_id`: Filter by team
- `project_id`: Filter by project

### Analytics

#### GET /api/analytics/dashboard
Get dashboard analytics (admin only).

**Query Parameters:**
- `days`: Number of days to analyze (default: 30)

**Response:**
```json
{
  "overview": {
    "total_users": 10,
    "total_teams": 3,
    "total_projects": 5,
    "active_projects": 4,
    "total_checkins": 25,
    "recent_checkins": 8
  },
  "averages": {
    "mood": 3.8,
    "workload": 3.2,
    "stress": 2.5
  }
}
```

## Error Handling

The API returns consistent error responses:

```json
{
  "message": "Error description",
  "error": "Detailed error information"
}
```

Common HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `409`: Conflict
- `500`: Internal Server Error

## Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <jwt_token>
```

## Role-Based Access

- **Admin**: Full access to all endpoints
- **Employee**: Limited access to own data and assigned projects

## Database Migrations

To create a new migration:

```bash
flask db migrate -m "Description of changes"
flask db upgrade
```

## Testing

Run tests (when implemented):

```bash
python -m pytest
```

## Deployment

### Production Checklist

1. **Environment Variables**
   - Set `FLASK_ENV=production`
   - Use strong `SECRET_KEY` and `JWT_SECRET_KEY`
   - Configure production database URL

2. **Database**
   - Set up PostgreSQL in production
   - Run migrations: `flask db upgrade`

3. **Security**
   - Enable HTTPS
   - Configure CORS origins properly
   - Use environment variables for secrets

4. **Performance**
   - Use a production WSGI server (Gunicorn)
   - Configure database connection pooling
   - Set up monitoring and logging

### Example Gunicorn Configuration

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Development

### Running in Development Mode

```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python app.py
```

### Database Reset

To reset the database with sample data:

```bash
# Drop and recreate database
dropdb teampulse_db
createdb teampulse_db

# Run application (creates tables and sample data)
python app.py
```

## Default Users

The application creates these default users on first run:

- **Admin**: `admin@teampulse.com` / `admin123`
- **Employee**: `employee@teampulse.com` / `employee123`

## Contributing

1. Follow PEP 8 style guidelines
2. Add docstrings to new functions
3. Write tests for new features
4. Update API documentation

## License

MIT License 