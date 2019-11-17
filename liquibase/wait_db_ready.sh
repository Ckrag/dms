DB_HOST="flask_db"
DB_PORT="5432"

while ! pg_isready -h ${DB_HOST} -p ${DB_PORT} > /dev/null 2> /dev/null; do
    echo "Pre-liquid-test: Connecting to ${DB_HOST} Failed"
    sleep 1
  done

