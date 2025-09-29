# Contributing to RecruitAI Pro

Thanks for taking the time to contribute!

## How to Contribute
1. Fork the repo and create your branch from `main` (or `dev` if it exists).
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Make your changes with tests where applicable.
4. Lint/Build:
   - Frontend: `cd frontend && npm install && npm run build`
   - Backend: `cd backend && python -m py_compile $(git ls-files '*.py')`
5. Commit with a clear message: `feat:`, `fix:`, `docs:`, `chore:` …
6. Push and open a Pull Request (PR) against `main`.

## Code Style
- Frontend: follow ESLint/Prettier defaults (Vite/Element Plus conventions).
- Backend: Python 3.11, type hints preferred; keep functions small and explicit.

## Pull Requests
- Keep PRs focused and small when possible.
- Include a brief description, screenshots for UI changes, and test notes.

## Issues
- Use labels: `bug`, `feature`, `docs`, `good first issue`, `help wanted`.
- Provide steps to reproduce for bugs and expected behavior.

## Security
- Do not include secrets in code. Use `.env` locally and `env.txt` as template.
- See `SECURITY.md` for reporting vulnerabilities.

## License
By contributing, you agree that your contributions will be licensed under the MIT License.
