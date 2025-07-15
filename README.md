# TeamPulse

A comprehensive internal tool for small teams and companies to track employee check-ins, morale, and project status. Built with Flask (Python) backend and React (TypeScript) frontend.

## Features

### 🔐 Authentication & Authorization
- Secure JWT-based authentication
- Role-based access control (Admin/Employee)
- Protected routes and API endpoints

### 👥 User Management
- Admin can create, update, and manage users
- Team assignments and role management
- User profile management

### 🏢 Team Management
- Create and manage teams
- Assign users to teams
- Team-based analytics and insights

### 📊 Project Management
- Create and track projects
- Assign users to projects
- Project status and priority tracking
- Due date management

### 📝 Check-in System
- Weekly employee check-ins
- Mood rating (1-5 scale)
- Workload and stress level tracking
- Optional comments and feedback

### 📈 Analytics Dashboard
- Team morale analytics
- Project performance insights
- Trend analysis over time
- Export capabilities

## Tech Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT with Flask-JWT-Extended
- **Password Hashing**: Flask-Bcrypt
- **CORS**: Flask-CORS
- **Migrations**: Flask-Migrate

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui (Radix UI)
- **Routing**: React Router DOM
- **Forms**: React Hook Form with Zod validation
- **Charts**: Recharts
- **Icons**: Lucide React

## Project Structure

```
TeamPulse/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Configuration management
│   ├── requirements.txt       # Python dependencies
│   ├── env.example           # Environment variables template
│   ├── models/               # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── team.py
│   │   ├── project.py
│   │   └── checkin.py
│   ├── auth/                 # Authentication utilities
│   │   ├── __init__.py
│   │   ├── jwt_auth.py
│   │   └── decorators.py
│   └── routes/               # API routes
│       ├── __init__.py
│       ├── auth_routes.py
│       ├── user_routes.py
│       ├── team_routes.py
│       ├── project_routes.py
│       ├── checkin_routes.py
│       └── analytics_routes.py
├── frontend/
│   ├── package.json          # Node.js dependencies
│   ├── vite.config.ts        # Vite configuration
│   ├── tailwind.config.js    # Tailwind CSS configuration
│   ├── tsconfig.json         # TypeScript configuration
│   └── src/
│       ├── main.tsx          # React entry point
│       ├── App.tsx           # Main App component
│       ├── index.css         # Global styles
│       ├── contexts/         # React contexts
│       ├── components/       # Reusable components
│       ├── pages/            # Page components
│       ├── hooks/            # Custom React hooks
│       ├── lib/              # Utility functions
│       └── types/            # TypeScript type definitions
└── README.md                 # This file
```

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- PostgreSQL

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd TeamPulse
   ```

2. **Set up Python environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your database and JWT settings
   ```

4. **Set up database**
   ```bash
   # Create PostgreSQL database
   createdb teampulse_db
   
   # Initialize database
   python app.py
   ```

5. **Run the backend**
   ```bash
   python app.py
   ```
   The API will be available at `http://localhost:5000`

### Frontend Setup

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Run the development server**
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - Register new user (admin only)
- `GET /api/auth/me` - Get current user info
- `PUT /api/auth/change-password` - Change password

### Users
- `GET /api/users` - Get all users (admin only)
- `GET /api/users/:id` - Get specific user
- `PUT /api/users/:id` - Update user (admin only)
- `DELETE /api/users/:id` - Delete user (admin only)
- `GET /api/users/profile` - Get current user profile
- `PUT /api/users/profile` - Update current user profile

### Teams
- `GET /api/teams` - Get all teams (admin only)
- `GET /api/teams/:id` - Get specific team
- `POST /api/teams` - Create team (admin only)
- `PUT /api/teams/:id` - Update team (admin only)
- `DELETE /api/teams/:id` - Delete team (admin only)
- `GET /api/teams/:id/members` - Get team members
- `POST /api/teams/:id/members/:user_id` - Add member to team
- `DELETE /api/teams/:id/members/:user_id` - Remove member from team

### Projects
- `GET /api/projects` - Get projects (filtered by role)
- `GET /api/projects/:id` - Get specific project
- `POST /api/projects` - Create project (admin only)
- `PUT /api/projects/:id` - Update project (admin only)
- `DELETE /api/projects/:id` - Delete project (admin only)
- `POST /api/projects/:id/assign/:user_id` - Assign user to project
- `DELETE /api/projects/:id/unassign/:user_id` - Unassign user from project

### Check-ins
- `GET /api/checkins` - Get all check-ins (admin only)
- `GET /api/checkins/my-checkins` - Get current user's check-ins
- `POST /api/checkins` - Create check-in
- `GET /api/checkins/:id` - Get specific check-in
- `PUT /api/checkins/:id` - Update check-in
- `DELETE /api/checkins/:id` - Delete check-in (admin only)
- `GET /api/checkins/weekly-summary` - Get weekly summary (admin only)

### Analytics
- `GET /api/analytics/dashboard` - Dashboard analytics (admin only)
- `GET /api/analytics/teams` - Team analytics (admin only)
- `GET /api/analytics/projects` - Project analytics (admin only)
- `GET /api/analytics/trends` - Mood trends (admin only)

## Default Users

When you first run the application, these default users are created:

- **Admin**: `admin@teampulse.com` / `admin123`
- **Employee**: `employee@teampulse.com` / `employee123`

## Deployment

### Backend (Render)
1. Connect your GitHub repository to Render
2. Set environment variables in Render dashboard
3. Deploy as a Python web service

### Frontend (Netlify)
1. Connect your GitHub repository to Netlify
2. Set build command: `npm run build`
3. Set publish directory: `dist`
4. Add environment variables in Netlify dashboard
5. Deploy

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue in the GitHub repository. 