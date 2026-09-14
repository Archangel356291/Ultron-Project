# Build context is the project root (see ../docker-compose.yml) because
# app.py serves ultron-dashboard.html from one directory above itself.

FROM docker:27-cli AS dockercli

FROM python:3.12-slim
COPY --from=dockercli /usr/local/bin/docker /usr/local/bin/docker

WORKDIR /app
COPY ultron-backend/requirements.txt ultron-backend/requirements.txt
RUN pip install --no-cache-dir -r ultron-backend/requirements.txt

COPY ultron-backend/ ultron-backend/
COPY ultron-dashboard.html ultron-dashboard.html

WORKDIR /app/ultron-backend
EXPOSE 5000
CMD ["python", "app.py"]
