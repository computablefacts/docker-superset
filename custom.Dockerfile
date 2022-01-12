FROM computablefacts/superset-for-swarm:1.3.2

# Copy requirements (database drivers)
COPY custom/requirements-local.txt /app/docker/requirements-local.txt

# Copy specific config
COPY custom/pythonpath/superset_config_docker.py /app/pythonpath/superset_config_docker.py
