# Contributing to InventoryManager95

First off, thank you for considering contributing to InventoryManager95! It's people like you that make InventoryManager95 such a great tool.

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct. Please report unacceptable behavior to support@inventorymanager95.com.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* Use a clear and descriptive title
* Describe the exact steps which reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed after following the steps
* Explain which behavior you expected to see instead and why
* Include screenshots if possible

### Suggesting Enhancements

If you have a suggestion for the project, we'd love to hear it. Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* A clear and descriptive title
* A detailed description of the proposed feature
* Any possible drawbacks or challenges you foresee
* If possible, a rough proposal of how to implement it

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code follows the existing style guidelines
6. Issue that pull request!

## Development Process

1. Clone the repository
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes
4. Write or adapt tests as needed
5. Update documentation as needed
6. Push to your fork and submit a pull request

### Development Setup

Please refer to the README.md for detailed setup instructions. In general, you'll need:

1. Python 3.8+
2. Node.js 18+
3. PostgreSQL
4. Git

### Code Style

#### Python (Backend)
- Follow PEP 8 guidelines
- Use Black for code formatting
- Use isort for import sorting
- Maximum line length of 88 characters (Black default)

#### JavaScript/TypeScript (Frontend)
- Use ESLint with our provided configuration
- Use Prettier for code formatting
- Follow React best practices and hooks guidelines

### Testing

- Write tests for new features
- Maintain or improve test coverage
- Run the full test suite before submitting PRs

#### Running Tests
```bash
# Backend tests
pytest

# Frontend tests
cd inventory-management-ui
npm test
```

### Documentation

- Update README.md if you change functionality
- Comment your code where necessary
- Update API documentation for endpoint changes
- Add JSDoc comments for new frontend components

## Community

- Join our Discord server for discussions
- Follow our blog for updates
- Attend our monthly community calls

## Questions?

Feel free to contact the development team at dev@inventorymanager95.com
