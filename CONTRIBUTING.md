# Contributing to Whistleblower Reporting System

Thank you for your interest in contributing to the Whistleblower Reporting System! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/whistleblower-system.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit your changes: `git commit -m "Add your feature"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- Git

### Setup Steps

1. Copy environment file:
   ```bash
   cp .env.example .env
   ```

2. Start development environment:
   ```bash
   docker-compose up --build
   ```

3. Run migrations:
   ```bash
   docker-compose exec backend python manage.py migrate
   ```

4. Create superuser (optional):
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

## Code Style

### Backend (Python/Django)

- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused
- Use type hints where appropriate

Run code formatting:
```bash
docker-compose exec backend black .
docker-compose exec backend flake8
```

### Frontend (TypeScript/React)

- Follow TypeScript best practices
- Use functional components with hooks
- Keep components small and reusable
- Use meaningful prop and variable names
- Add TypeScript types for all props and state

Run linting:
```bash
docker-compose exec frontend npm run lint
```

## Testing

### Backend Tests

All new features should include tests:

- Unit tests for models
- Unit tests for serializers
- Integration tests for API endpoints
- Permission tests for data segregation

Run tests:
```bash
docker-compose exec backend pytest
docker-compose exec backend pytest --cov  # With coverage
```

### Frontend Tests

(Can be added in future iterations)

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Update the API documentation if you're changing endpoints
3. Ensure all tests pass
4. Update the changelog (if applicable)
5. Request review from maintainers
6. Address any feedback from code review

## Pull Request Guidelines

- Keep PRs focused on a single feature or bug fix
- Write clear, descriptive commit messages
- Reference any related issues in your PR description
- Include screenshots for UI changes
- Ensure your code passes all tests
- Update documentation as needed

## Reporting Bugs

When reporting bugs, please include:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment details (OS, browser, etc.)

## Suggesting Enhancements

When suggesting enhancements, please include:

- A clear, descriptive title
- Detailed description of the proposed feature
- Use cases and benefits
- Potential implementation approach (optional)

## Security Issues

**Do not report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability, please email the maintainers directly. Include:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

## Code Review Process

All submissions require review. We use GitHub pull requests for this purpose. Reviewers will check:

- Code quality and style
- Test coverage
- Documentation updates
- Security considerations
- Performance implications

## Community Guidelines

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Follow the project's code of conduct

## Questions?

If you have questions, feel free to:
- Open an issue for discussion
- Contact the maintainers
- Check existing documentation

Thank you for contributing to making workplaces safer and more transparent!
