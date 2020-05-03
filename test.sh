if [[ $# -eq 0 ]] ; then
    echo 'No path to project root supplieds'
    exit 1
fi


# Setup sql, later will be liquibase
DIR_PATH=$1

STALL=${2:-false}

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
-p 9999:5432 \
postgres

while ! pg_isready -h 0.0.0.0 -p 9999 > /dev/null 2> /dev/null; do
    echo "BUMP"
    sleep 1
  done

# build DB
PGPASSWORD=root psql -U root -p 9999 -h 0.0.0.0 -c 'CREATE DATABASE dms;'
PGPASSWORD=root psql -U root -p 9999 -h 0.0.0.0 -d 'dms' -f $DIR_PATH/db/init.sql

#(export FOO=bar && somecommand someargs | somecommand2)

CONN_STR="postgresql://0.0.0.0:9999/dms?user=root&password=root"

export DMS_TEST_DB_STRING=$CONN_STR


if [[ $STALL = true ]]
then
  echo "the env var is: DMS_TEST_DB_STRING=${CONN_STR}"
  read -p "Press any key to end test session"
else
  echo "Running tests"
	#python3 ./grafana-app/test.py "postgresql://0.0.0.0:9999/dms?user=root&password=root"
	#python3 ./flask-app/test.py "postgresql://0.0.0.0:9999/dms?user=root&password=root"
	(cd flask-app && python3 -m unittest discover test)
	echo "Tests complete"
fi


unset DMS_TEST_DB_STRING