

# Project Standards

This project is an e-commerce cart management system. It has a Python/FastAPI backend and a React frontend.

## Quick Commands

- **Run Backend Dev Server**: `uvicorn main:app --reload`
- **Run Backend Tests**: `testenv\Scripts\pytest test_main.py`
- **Run Frontend Dev Server**: `npm --prefix frontend start` (react-scripts) or `npm --prefix frontend/my-react-app run dev` (Vite)
- **Run Frontend Tests**: `$env:CI="true"; npm --prefix frontend test` (PowerShell)

---

@.claude/standards/testing.md

## Tech Stack & Language Standards

### Backend (Python)
- Use Python 3.12+
- Follow PEP 8 style guidelines.
- Use FastAPI for building API endpoints.
- Use Pydantic models for validation and SQLAlchemy for ORM.
- Use meaningful variable and function names.
- Add docstrings for public functions.

### Frontend (React / JS)
- Use React 18+ (Functional components, hooks).
- Use Axios for API communication.
- Use Vanilla CSS for styling.
- Keep components modular and reusable.

## API Patterns

- Return JSON responses.
- Validate inputs using Pydantic models.
- Handle errors using structured responses.
- Never hardcode secrets or DB credentials in production (load from environment variables).

## Code Quality

- Keep functions/components small and focused.
- Write readable, maintainable code.
- Avoid duplicate logic.
- Use comments only when necessary to explain complex logic.
