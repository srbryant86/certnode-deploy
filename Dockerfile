
# CertNode Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . /app
RUN pip install flask

EXPOSE 8080
CMD ["python", "api_server.py"]
