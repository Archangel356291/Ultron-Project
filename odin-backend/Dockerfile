# Build context is the project root (see ../docker-compose.yml) because
# app.py serves ultron-dashboard.html from one directory above itself.

FROM docker:27-cli AS dockercli

FROM python:3.12-slim
COPY --from=dockercli /usr/local/bin/docker /usr/local/bin/docker

WORKDIR /app
COPY odin-backend/requirements.txt odin-backend/requirements.txt
RUN pip install --no-cache-dir -r odin-backend/requirements.txt

COPY odin-backend/ odin-backend/
COPY ultron-dashboard.html ultron-dashboard.html
# Installable-app service worker, served (versioned) by /sw.js in app.py.
COPY sw.js sw.js
# Module 13: vendored Three.js + the built hero-head .glb, served by the new
# /three-pipeline/<file> route in app.py.
COPY three-pipeline/ three-pipeline/
# Pixel-art sprites/backdrop for the Odin tab, served by /pixel-assets/<file>.
COPY pixel-assets/ pixel-assets/
# Self-hosted dashboard typefaces (OFL), served by /fonts/<file>.
COPY fonts/ fonts/
# Home-tab knowledge graph: only graph.json itself (already privacy-redacted
# by Module 4) -- not the rest of graphify-out/ (caches, the Obsidian export,
# the never-committed private-nodes.enc.json), read server-side by
# get_knowledge_graph() in app.py, not served as a raw static file.
COPY graphify-out/graph.json graphify-out/graph.json

# Not root: nothing here needs it. Everything the app writes goes to the
# /data mount. The Docker socket is the one thing a plain user cannot open;
# docker-compose.yml grants that through group_add rather than by keeping
# root (see the note there).
RUN useradd --uid 10001 --no-create-home --shell /usr/sbin/nologin odin
USER odin

WORKDIR /app/odin-backend
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=10s --start-period=25s --retries=3 CMD ["python", "healthcheck.py"]
# gunicorn, not `python app.py` (Flask's development server) -- see
# gunicorn.conf.py for why it is one worker with many threads.
CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]
