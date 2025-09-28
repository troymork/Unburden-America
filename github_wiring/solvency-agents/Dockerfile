# syntax=docker/dockerfile:1
FROM python:3.11-slim
WORKDIR /app
COPY server.py .
RUN pip install fastapi uvicorn pydantic
EXPOSE 8080
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
