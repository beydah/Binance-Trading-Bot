# Contributing to Binance Trading Bot

Thank you for your interest in contributing to the Binance Trading Bot! We welcome all contributions from the community.

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Making Changes](#making-changes)
5. [Pull Request Process](#pull-request-process)
6. [Reporting Issues](#reporting-issues)
7. [Feature Requests](#feature-requests)
8. [Code Style](#code-style)
9. [Testing](#testing)
10. [Documentation](#documentation)
11. [Community](#community)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

1. Fork the repository on GitHub
2. Clone your forked repository to your local machine
3. Install the required dependencies (see Development Setup)
4. Create a new branch for your changes

## Development Setup

1. Ensure you have Python 3.8+ installed
2. Set up a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your environment variables by creating a `.env` file with your API keys:
   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   TELEGRAM_USER_ID=your_telegram_user_id
   BINANCE_API_KEY=your_binance_api_key
   BINANCE_API_SECRET=your_binance_api_secret
   ```

## Making Changes

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b bugfix/issue-description
   ```
2. Make your changes following the code style guidelines
3. Add tests for your changes (if applicable)
4. Update the documentation if needed
5. Run the tests to ensure everything works

## Pull Request Process

1. Ensure your code follows the project's coding standards
2. Update the README.md with details of changes if needed
3. Run all tests and ensure they pass
4. Submit a pull request with a clear description of the changes
5. Reference any related issues in your PR description
6. Wait for the maintainers to review your PR

## Reporting Issues

When reporting issues, please include:
- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Screenshots if applicable
- Your environment (OS, Python version, etc.)
- Any error messages

## Feature Requests

We welcome feature requests! Please open an issue with:
- A clear description of the feature
- The problem it solves
- Any alternative solutions you've considered
- Additional context or screenshots

## Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines
- Use 4 spaces for indentation
- Keep lines under 120 characters
- Use descriptive variable and function names
- Add type hints for function parameters and return values
- Include docstrings for all public functions and classes

## Testing

1. Run the test suite:
   ```bash
   # Add test command here when tests are available
   ```
2. Ensure all tests pass before submitting a PR
3. Add new tests for new features or bug fixes

## Documentation

- Keep the documentation up-to-date with your changes
- Use clear and concise language
- Add comments to explain complex logic
- Update the README.md if your changes affect the setup or usage

## Community

- Join our [Discord/Telegram] community [link] (if available)
- Help answer questions from other users
- Review pull requests and issues
- Share your ideas and feedback

## License

By contributing, you agree that your contributions will be licensed under the project's [LICENSE](LICENSE) file.
