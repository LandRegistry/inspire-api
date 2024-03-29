# Set the base image to the s2i image
FROM docker-registry/stp/stp-s2i-python-extended:3.9

# Development environment values
# These values are not the same as our production environment
ENV APP_NAME="inspire-api" \
    SQL_HOST="postgres-13" \
    LOG_LEVEL="DEBUG" \
    COMMIT="LOCAL" \
    SQL_DATABASE="llc_inspire" \
    SQL_PASSWORD="inspirepassword" \
    APP_SQL_USERNAME="inspireuser" \
    AUTHENTICATION_API_URL="http://authentication-api:8080/v2.0" \
    AUTHENTICATION_API_ROOT="http://authentication-api:8080" \
    ALEMBIC_SQL_USERNAME="root" \
    SQL_USE_ALEMBIC_USER="false" \
    SQLALCHEMY_POOL_RECYCLE="3300" \
    MAX_HEALTH_CASCADE=6 \
    APP_MODULE='inspire_api.main:app' \
    FLASK_APP='inspire_api.main' \
    GUNICORN_ARGS='--reload' \
    WEB_CONCURRENCY='2' \
    PYTHONPATH=/src

# Switch from s2i's non-root user back to root for the following commmands
USER root

# Create a user that matches dev-env runner's host user
# And ensure they have access to the jar folder at runtime
ARG OUTSIDE_UID
ARG OUTSIDE_GID
RUN groupadd --force --gid $OUTSIDE_GID containergroup && \
    useradd --uid $OUTSIDE_UID --gid $OUTSIDE_GID containeruser

ADD requirements_test.txt requirements_test.txt
ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt && \
    pip3 install -r requirements_test.txt

# Set the user back to a non-root user like the s2i run script expects
# When creating files inside the docker container, this will also prevent the files being owned
# by the root user, which would cause issues if running on a Linux host machine
USER containeruser

CMD ["/usr/libexec/s2i/run"]
