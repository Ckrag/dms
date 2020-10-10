if [[ $# -eq 0 ]] ; then
    echo 'No path to project root supplieds'
    exit 1
fi


# Setup sql, later will be liquibase
DIR_PATH=$1

STALL=${2:-false}

DB_HOST="0.0.0.0"
DB_USER="root"
DB_PASS="root"
DB_PORT="9999"
DB_SCHEMA="dms"

# REMEMBER TO: sudo apt install postgresql for pg_isready
# https://www.postgresql.org/docs/9.3/app-pg-isready.html

# Cleanup
set -e # https://stackoverflow.com/a/56302691
remove_container() {
	docker container stop $(docker container ls -q --filter name=pg-docker)
}
trap remove_container EXIT

docker run \
--rm \
--name pg-docker \
-it \
-e POSTGRES_USER=root \
-e POSTGRES_PASSWORD=root \
-d \
-p $DB_PORT:5432 \
postgres

while ! pg_isready -h $DB_HOST -p $DB_PORT > /dev/null 2> /dev/null; do
    echo "BUMP"
    sleep 1
  done

# build DB
PGPASSWORD=$DB_PASS psql -U $DB_USER -p $DB_PORT -h $DB_HOST -c "CREATE DATABASE $DB_SCHEMA;"
PGPASSWORD=$DB_PASS psql -U $DB_USER -p $DB_PORT -h $DB_HOST -d $DB_SCHEMA -f $DIR_PATH/db/1_init.sql
PGPASSWORD=$DB_PASS psql -U $DB_USER -p $DB_PORT -h $DB_HOST -d $DB_SCHEMA -f $DIR_PATH/db/2_config.sql

#(export FOO=bar && somecommand someargs | somecommand2)

CONN_STR="postgresql://$DB_HOST:$DB_PORT/$DB_SCHEMA?user=$DB_USER&password=$DB_PASS"

export DMS_TEST_DB_STRING=$CONN_STR


if [[ $STALL = true ]]
then
  echo "the env var is: DMS_TEST_DB_STRING=${CONN_STR}"
  echo "psql string: psql -h $DB_HOST -U $DB_USER -p $DB_PORT $DB_SCHEMA"
  read -p "Press any key to end test session"
else
  echo "Running tests"
	python3 ./grafana-app/test.py $CONN_STR
	(cd flask-app && python3 -m unittest discover test)
	echo "Tests complete"
fi


unset DMS_TEST_DB_STRING