DB_NAME=dvdrental
PG_FILE=dvdrental.tar
MASTER_DB=postgres
PG_USER=postgres

CONTAINER_NAME=${1}

if [[ -z "$CONTAINER_NAME" ]]; then
    echo "Please specify a container name"
    exit 1
fi

CONTAINER_ID=$(docker ps --format='{{.ID}}' --filter name=^/$CONTAINER_NAME)

docker cp ${PG_FILE} ${CONTAINER_ID}:/dump.db

docker exec -it $CONTAINER_ID bash -c "dropdb -U $PG_USER -f --if-exists $DB_NAME"
docker exec -it $CONTAINER_ID bash -c "createdb $DB_NAME -U $PG_USER"
docker exec -it $CONTAINER_ID bash -c "pg_restore -U $PG_USER -d $DB_NAME ./dump.db"
