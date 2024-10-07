FROM computablefacts/superset-for-swarm:4.0.2

# Switching to root to install the required packages
USER root

# Install webdriver for report generation
# See: https://github.com/apache/superset/issues/7466#issuecomment-490148436
# See: https://superset.apache.org/docs/installation/alerts-reports/#using-firefox
RUN apt-get update && \
    apt-get install --no-install-recommends -y firefox-esr wget

ENV GECKODRIVER_VERSION=0.29.0
RUN wget -q https://github.com/mozilla/geckodriver/releases/download/v${GECKODRIVER_VERSION}/geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz && \
    tar -x geckodriver -zf geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz -O > /usr/bin/geckodriver && \
    chmod 755 /usr/bin/geckodriver && \
    rm geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz

RUN pip install --no-cache gevent psycopg2 redis watchdog

COPY custom/docker-bootstrap.sh /app/docker/docker-bootstrap.sh
RUN chmod +x /app/docker/*.sh

# Patch for changing report email title
# See: https://github.com/apache/superset/blob/994de1f81218f1f550132b67c32e88a942eec8b7/superset/commands/report/execute.py#L440
RUN sed -i 's/f"{self._report_schedule.name}: "/f"{self._report_schedule.name}"/' /app/superset/commands/report/execute.py
RUN sed -i 's/f"{self._report_schedule.chart.slice_name}"//' /app/superset/commands/report/execute.py
RUN sed -i 's/f"{self._report_schedule.dashboard.dashboard_title}"//' /app/superset/commands/report/execute.py

# Patch for removing link to Superset from report email
# See: https://github.com/apache/superset/blob/994de1f81218f1f550132b67c32e88a942eec8b7/superset/reports/notifications/email.py#L163
RUN sed -i 's#<b><a href="{self._content.url}">{call_to_action}</a></b><p></p>#<p></p>#' /app/superset/reports/notifications/email.py

# Patch a migration from 1.4 to 1.5
# See: https://github.com/apache/superset/issues/20685
# The issue is solved but not yet included in version 1.5.2
#RUN sed -i 's/except sa.exc.OperationalError:/except (sa.exc.OperationalError, sa.exc.DatabaseError):/' /app/superset/migrations/versions/b92d69a6643c_rename_csv_to_file.py

# Switching back to using the `superset` user
USER superset

# Copy requirements (database drivers)
COPY custom/requirements-local.txt /app/docker/requirements-local.txt

# Copy specific config
COPY --chown=superset:superset custom/pythonpath/ /app/pythonpath/

COPY custom/images/* /app/superset/static/assets/images/
