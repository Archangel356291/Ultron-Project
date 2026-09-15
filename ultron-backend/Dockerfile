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
# Module 13: vendored Three.js + the built hero-head .glb, served by the new
# /three-pipeline/<file> route in app.py.
COPY three-pipeline/ three-pipeline/
# Home-tab knowledge graph: only graph.json itself (already privacy-redacted
# by Module 4) -- not the rest of graphify-out/ (caches, the Obsidian export,
# the never-committed private-nodes.enc.json), read server-side by
# get_knowledge_graph() in app.py, not served as a raw static file.
COPY graphify-out/graph.json graphify-out/graph.json

WORKDIR /app/ultron-backend
EXPOSE 5000
CMD ["python", "app.py"]
