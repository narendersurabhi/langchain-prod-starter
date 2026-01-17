FROM python:3.12-slim AS builder

WORKDIR /app
COPY pyproject.toml README.md /app/
COPY src /app/src
RUN pip install --upgrade pip && pip install build
RUN python -m build --wheel

FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN addgroup --system app && adduser --system --ingroup app app

COPY --from=builder /app/dist/*.whl /app/
RUN pip install --no-cache-dir /app/*.whl

USER app
EXPOSE 8000

CMD ["uvicorn", "lc_app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
