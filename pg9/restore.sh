#!/bin/bash
# TODO: Store your POSTGRES_USER and POSTGRES_DB variables in .env
# (also add .env to .gitignore)
source .env

PG_FILE=${1}
DB_NAME=${2}

if [[ -z "$PG_FILE" ]]; then
    echo "Please specify a PostgreSQL file"
    exit 1
fi

if [[ -z "$DB_NAME" ]]; then
   echo "Please specify a database name"
   exit 1
fi

# TODO: replace/leave off somename.
CONTAINER_ID=$(docker ps --format='{{.ID}}' --filter name=^/pg9)

docker cp ${PG_FILE} ${CONTAINER_ID}:/dump.db

docker exec -e DB_NAME=${DB_NAME} -it $CONTAINER_ID bash -c 'pg_restore -c -U ${POSTGRES_USER} -d $DB_NAME ./dump.db'
