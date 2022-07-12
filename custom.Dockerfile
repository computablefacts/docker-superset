FROM computablefacts/superset-for-swarm:1.5.1

# Switching to root to install the required packages
USER root

# Install webdriver for report generation
# See: https://github.com/apache/superset/issues/7466#issuecomment-490148436
# See: https://superset.apache.org/docs/installation/alerts-reports/#using-firefox
RUN apt-get update && \
    apt-get install --no-install-recommends -y firefox-esr

ENV GECKODRIVER_VERSION=0.29.0
RUN wget -q https://github.com/mozilla/geckodriver/releases/download/v${GECKODRIVER_VERSION}/geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz && \
    tar -x geckodriver -zf geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz -O > /usr/bin/geckodriver && \
    chmod 755 /usr/bin/geckodriver && \
    rm geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz

RUN pip install --no-cache gevent psycopg2 redis

# Switching back to using the `superset` user
USER superset

# Copy requirements (database drivers)
COPY custom/requirements-local.txt /app/docker/requirements-local.txt

# Copy specific config
COPY custom/pythonpath/ /app/pythonpath/

COPY custom/images/cf-logo.png /app/superset/static/assets/images/cf-logo.png
COPY custom/images/loading.gif /app/superset/static/assets/images/loading.gif
