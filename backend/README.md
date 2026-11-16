# Hawinet FastAPI Backend

This directory contains the existing FastAPI application and tests relocated from the repository root. The source files under `app/` and `tests/` were not edited as part of the move.

Install dependencies from `requirements.txt`, configure `DATABASE_URL` using `.env.example`, then run:

```bash
python -m uvicorn app.main:app --reload
```

Run tests with `pytest`.
