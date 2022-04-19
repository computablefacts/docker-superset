FROM computablefacts/superset-for-swarm:1.4.2

# Copy requirements (database drivers)
COPY custom/requirements-local.txt /app/docker/requirements-local.txt

# Copy specific config
COPY custom/pythonpath/ /app/pythonpath/

COPY custom/images/cf-logo.png /app/superset/static/assets/images/cf-logo.png
COPY custom/images/loading.gif /app/superset/static/assets/images/loading.gif
