# Setup sql, later will be liquibase
DIR_PATH=$1
TEST=$2

docker run \
--rm \
--name pg-docker \
-it \
-e POSTGRES_USER=root \
-d \
-p 9999:5432 \
postgres

while ! pg_isready -h 0.0.0.0 -p 9999 > /dev/null 2> /dev/null; do
    echo "BUMP"
    sleep 1
  done

# build DB
psql -U root -p 9999 -h 0.0.0.0 -f $DIR_PATH/db/init.sql

#for f in grafana-app/test/*.py; do python3 "$f"; done
eval $TEST

# Cleanup
docker container stop $(docker container ls -q --filter name=pg-docker)