# Contributing to Binance Trading Bot

Thank you for considering contributing to the Binance Trading Bot! We welcome all forms of contribution, from bug reports and feature requests to code improvements and documentation updates.

## Getting Started

1.  **Fork** the repository on GitHub.
2.  **Clone** your fork locally:
    ```bash
    git clone https://github.com/your-username/Binance-Trading-Bot.git
    cd Binance-Trading-Bot
    ```
3.  **Create a new branch** for your feature or fix:
    ```bash
    git checkout -b feature/amazing-feature
    ```

## Development Setup

1.  **Prerequisites**: Python 3.10+
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configuration**:
    -   Copy `.env.example` to `.env`.
    -   Fill in your API keys (for local testing, you can use dummy values if running unit tests).

## Code Standards

We strive for clean, maintainable, and modern Python code.

-   **Style**: Follow [PEP 8](https://peps.python.org/pep-0008/).
-   **Type Hinting**: Use type hints for all function arguments and return values.
-   **Configuration**: Use `src/config.py` for all settings. partial hardcoding is not allowed.
-   **Logging**: Use `src/utils/logger.py` (`logger.info`, `logger.error`) instead of `print()`.

## Running Tests

Before submitting a Pull Request, ensure all tests pass:

```bash
pytest tests/
```

If you add new functionality, please add corresponding unit tests in the `tests/` directory.

## Submitting a Pull Request

1.  Push your branch to GitHub.
2.  Open a Pull Request against the `main` branch.
3.  Describe your changes clearly in the PR description.
4.  Link any related issues (e.g., `Fixes #123`).

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
