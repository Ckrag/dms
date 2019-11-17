DB_HOST="flask_db"
DB_PORT="5432"

#while !</dev/tcp/db/5432; do sleep 1; done;

#while ! nc -z ${DB_HOST} ${DB_PORT}; do sleep 1; done;
# Almost done..
#sleep 10;



while ! pg_isready -h ${DB_HOST} -p ${DB_PORT} > /dev/null 2> /dev/null; do
    echo "Connecting to ${DB_HOST} Failed"
    sleep 1
  done

