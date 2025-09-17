# Contributing Guidelines

Thank you for your interest in improving the CPU Scheduling Simulator! This
project thrives on community feedback and pull requests. The following guidance
keeps the repository approachable for new contributors.

## Ways to Contribute

- **Report issues** – Describe bugs, confusing behaviour, or documentation gaps.
- **Improve docs** – Tutorials, diagrams, and clarifications are always welcome.
- **Enhance the simulator** – New scheduling algorithms, visualisations, or
  quality-of-life features such as exporting data.
- **Automate testing** – Adding unit tests or linting scripts would greatly
  benefit maintainability.

## Development Workflow

1. Fork the repository and create a feature branch (one logical change per
   branch keeps reviews focused).
2. Install dependencies with `pip install -r requirements.txt` and run the app
   locally via `python app.py`.
3. Make your changes and ensure the simulator still behaves as expected.
4. Update documentation and add tests if applicable.
5. Open a pull request summarising the motivation and key changes. Screenshots
   are encouraged when modifying the UI.

## Code Style

- The Python code targets **PEP 8** readability. Type hints and docstrings are
  encouraged for new functions.
- Keep templates self-contained; heavy JavaScript logic should live in separate
  files only if it grows substantially.
- Prefer small, focused commits with descriptive messages.

## Commit Message Format

While not mandatory, the following template works well:

```
<type>: <summary>

<body explaining the change>
```

Examples of types: `fix`, `feat`, `docs`, `refactor`, `chore`.

## Code of Conduct

This project adheres to the [Contributor Covenant](CODE_OF_CONDUCT.md). By
participating you agree to foster an open and respectful environment.

If you have questions before contributing, feel free to open an issue or start a
GitHub discussion. We are happy to help!

