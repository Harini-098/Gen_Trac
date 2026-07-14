
paths:
  - "**/test_*.py"
  - "**/*.test.js"
  - "**/*.test.jsx"

# Testing Rules

## Running Tests
- **Backend Tests (FastAPI)**:
  - Run using: `testenv\Scripts\pytest test_main.py` (or `pytest test_main.py` if the environment is activated).
- **Frontend Tests (React)**:
  - Run using: `$env:CI="true"; npm --prefix frontend test` (on Windows/PowerShell) or `CI=true npm --prefix frontend test`.

## Backend Testing Rules (FastAPI / pytest)
- Use `fastapi.testclient.TestClient` for API testing.
- Override database dependency using `app.dependency_overrides[get_db] = override_get_db`.
- Use a local/sqlite memory DB (e.g. `sqlite:///./test.db`) for testing.
- Use `pytest.fixture(autouse=True)` to create tables (`Base.metadata.create_all`) and seed initial data before each test, and drop tables (`Base.metadata.drop_all`) after each test.
- Test both success cases (e.g., status code 200/201, correct response payload) and failure/edge cases (e.g., product not found, invalid payloads).

## Frontend Testing Rules (React / Jest)
- Use React Testing Library (`@testing-library/react` and `@testing-library/jest-dom`).
- Query elements using accessible methods (e.g., `screen.getByText` with case-insensitive regular expressions where appropriate).
- Verify elements are rendered and interactions (like clicks or input) trigger expected behaviors.
- Mock external Axios/API calls where appropriate to keep unit tests isolated.
- Keep test cases clean, independent, and free of duplicate logic.