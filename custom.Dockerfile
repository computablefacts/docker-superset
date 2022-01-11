FROM computablefacts/superset-for-swarm:1.3.0

# Copy requirements (database drivers)
COPY custom/requirements-local.txt /app/docker/requirements-local.txt
