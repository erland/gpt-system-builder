FROM python:3.12-slim-bookworm

WORKDIR /app

RUN useradd --system --uid 10001 --create-home appuser

COPY src/app.py /app/app.py

ENV PORT=8080
EXPOSE 8080

USER appuser

ENTRYPOINT ["python", "/app/app.py"]
