FROM openjdk:8

RUN apt-get update && apt-get install -f -y postgresql-client

COPY liquibase /liquibase
COPY db /db

ENTRYPOINT liquibase/wait_db_ready.sh && \
  /liquibase/liquibase-3.8.1/liquibase \
  --driver=org.postgresql.Driver \
  --classpath=/liquibase/postgresql-42.2.8.jar \
  --url="jdbc:postgresql://flask_db:5432/dms?createDatabaseIfNotExist=true" \
  --changeLogFile=/liquibase/changeLog.xml \
  --username=root \
  --password=root \
  update
