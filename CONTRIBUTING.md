# Contributing to TeamPulse

Thank you for your interest in contributing to TeamPulse! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 18+
- PostgreSQL
- Git

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/TeamPulse.git
   cd TeamPulse
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp env.example .env
   # Edit .env with your settings
   createdb teampulse_db
   python app.py
   ```

3. **Set up the frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## 📋 Development Guidelines

### Code Style

#### Python (Backend)
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose
- Use type hints where appropriate

#### TypeScript (Frontend)
- Follow ESLint configuration
- Use meaningful component and variable names
- Add JSDoc comments for complex functions
- Keep components focused and reusable
- Use proper TypeScript types

### Git Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clear, descriptive commit messages
   - Keep commits focused and atomic
   - Test your changes thoroughly

3. **Push and create a pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Format

Use conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Examples:
- `feat(auth): add password reset functionality`
- `fix(api): resolve user creation validation error`
- `docs(readme): update deployment instructions`

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 📝 Pull Request Guidelines

### Before Submitting
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation is updated
- [ ] No console errors
- [ ] Responsive design works
- [ ] Cross-browser compatibility

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Backend tests pass
- [ ] Frontend tests pass
- [ ] Manual testing completed

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No console errors
```

## 🐛 Bug Reports

When reporting bugs, please include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Browser/OS information
- Screenshots if applicable

## 💡 Feature Requests

When requesting features, please include:
- Clear description of the feature
- Use case and benefits
- Mockups or examples if applicable
- Priority level

## 📚 Documentation

### Adding Documentation
- Update README.md for major changes
- Add inline comments for complex logic
- Update API documentation for new endpoints
- Include setup instructions for new features

### Documentation Standards
- Use clear, concise language
- Include code examples
- Add screenshots for UI features
- Keep documentation up to date

## 🔧 Development Tools

### Recommended VS Code Extensions
- Python
- TypeScript and JavaScript
- Tailwind CSS IntelliSense
- ESLint
- Prettier
- GitLens

### Useful Commands

#### Backend
```bash
# Run with debug mode
export FLASK_DEBUG=1
python app.py

# Reset database
dropdb teampulse_db && createdb teampulse_db && python app.py

# Check code style
flake8 .
```

#### Frontend
```bash
# Development server
npm run dev

# Build for production
npm run build

# Lint code
npm run lint

# Type checking
npx tsc --noEmit
```

## 🏗️ Architecture Guidelines

### Backend
- Keep routes focused and single-purpose
- Use blueprints for organization
- Implement proper error handling
- Follow RESTful API conventions
- Use database migrations for schema changes

### Frontend
- Use functional components with hooks
- Implement proper error boundaries
- Follow component composition patterns
- Use TypeScript for type safety
- Implement responsive design

## 🚀 Deployment

### Testing Deployment
- Test backend on Render
- Test frontend on Netlify
- Verify environment variables
- Check CORS configuration
- Test authentication flow

### Production Checklist
- [ ] Environment variables set
- [ ] Database migrations run
- [ ] SSL certificates configured
- [ ] Monitoring set up
- [ ] Error tracking configured

## 🤝 Community

### Getting Help
- Check existing issues and PRs
- Search documentation
- Ask questions in discussions
- Join community channels

### Code of Conduct
- Be respectful and inclusive
- Help others learn and grow
- Provide constructive feedback
- Follow project guidelines

## 📄 License

By contributing to TeamPulse, you agree that your contributions will be licensed under the MIT License.

## 🙏 Acknowledgments

Thank you for contributing to TeamPulse! Your contributions help make this project better for everyone. 