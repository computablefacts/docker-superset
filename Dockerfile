FROM apache/superset:1.4.0

# Switching to root to install the required packages
USER root

# Copy Docker specific scripts
COPY docker/*.sh /app/docker/
RUN chmod +x /app/docker/*.sh

# Copy Docker specific config
COPY docker/pythonpath/superset_config.py /app/pythonpath/superset_config.py

# Switching back to using the `superset` user
USER superset




