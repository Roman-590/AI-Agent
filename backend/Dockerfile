FROM python:3.11-slim

WORKDIR /app

COPY backend/pyproject.toml backend/poetry.lock* /app/

RUN pip install --no-cache-dir fastapi uvicorn[standard]

COPY backend/app /app/app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
