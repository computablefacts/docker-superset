FROM computablefacts/superset-for-swarm:1.5.2

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

# Patch for changing report email title
# See: https://github.com/apache/superset/blob/master/superset/reports/commands/execute.py#L363
RUN sed -i 's/f"{self._report_schedule.name}: "//' /app/superset/reports/commands/execute.py

# Patch for removing link to Superset from report email
# See: https://github.com/apache/superset/blob/master/superset/reports/notifications/email.py#L165
RUN sed -i 's#<b><a href="{url}">{call_to_action}</a></b><p></p>#<p></p>#' /app/superset/reports/notifications/email.py

# Patch a migration from 1.4 to 1.5
# See: https://github.com/apache/superset/issues/20685
# The issue is solved but not yet included in version 1.5.2
RUN sed -i 's/except sa.exc.OperationalError:/except (sa.exc.OperationalError, sa.exc.DatabaseError):/' /app/superset/migrations/versions/b92d69a6643c_rename_csv_to_file.py

# Switching back to using the `superset` user
USER superset

# Copy requirements (database drivers)
COPY custom/requirements-local.txt /app/docker/requirements-local.txt

# Copy specific config
COPY custom/pythonpath/ /app/pythonpath/

COPY custom/images/cf-logo.png /app/superset/static/assets/images/cf-logo.png
COPY custom/images/loading.gif /app/superset/static/assets/images/loading.gif
