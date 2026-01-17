# Contributing to Resume-Job Matcher

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone <your-fork-url>`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test thoroughly
6. Submit a pull request

## Development Setup

```bash
# Run the setup script
./setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd frontend && npm install
```

## Code Style

### Python
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small

### JavaScript/React
- Use functional components with hooks
- Follow React best practices
- Use meaningful component and variable names
- Keep components focused on single responsibility

### CSS
- Use Tailwind utility classes
- Follow the existing component patterns
- Keep custom CSS minimal

## Testing

Before submitting a PR:
1. Test the backend API endpoints
2. Test the frontend UI components
3. Test file upload with different formats
4. Test matching with various job descriptions
5. Ensure Docker build works: `docker-compose build`

## Areas for Contribution

### High Priority
- [ ] Unit tests for matching algorithms
- [ ] Integration tests for API endpoints
- [ ] Frontend component tests
- [ ] Performance optimization for large resumes
- [ ] Accessibility improvements

### Features
- [ ] LinkedIn job import
- [ ] Email notifications
- [ ] Resume tailoring suggestions
- [ ] Export match reports to PDF
- [ ] Browser extension
- [ ] Job board integrations

### Documentation
- [ ] API documentation with examples
- [ ] Video tutorials
- [ ] Deployment guides (AWS, Azure, GCP)
- [ ] Architecture documentation

## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update documentation for any API changes
3. Ensure all tests pass
4. Your PR should target the `main` branch
5. Add a clear description of what your PR does

## Code Review

All submissions require review. We'll look for:
- Code quality and style
- Test coverage
- Documentation
- Performance impact
- Security considerations

## Bug Reports

When filing a bug report, include:
- Clear description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots if applicable
- Environment details (OS, Python version, etc.)

## Feature Requests

For feature requests:
- Describe the feature and use case
- Explain why it would be valuable
- Consider implementation complexity
- Provide examples if possible

## Questions?

Feel free to open an issue for any questions or discussions!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

