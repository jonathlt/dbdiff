# Postgres Diff

## What?
This tool is intended to be used to compare postgres database schemas. Currently only comparing tables in the sense whether a table having a particular name appears in one database and not in another.

## Why?
I needed to be able to compare databases which were held in very different versions of postgres, namely versions 9 and 15. Comparing dumps of databases tended not to provide good results, so have decided to go down the route of comparing the outputs produced using queries.

## How to install command 'dbdiff' using pipx (local source)
* Install pipx
* Clone code

Then run
````     
    pipx install .
````

## How to configure
Set up a config.ini file similar to the one below. database1 and database2 credentials need to be populated. The [tablesquery] section can be left unchanged.

    [database1]
    host = localhost
    port = 5434
    database = dvdrental
    user = postgres
    password = mypassword


    [database2]
    host = localhost
    port = 5435
    database = dvdrental
    user = postgres
    password = mypassword

    [tablesquery]
    sqlfile = sql/tables.sql

    [functionsquery]
    sqlfile = sql/functions.sql

## How to run as a command
    Usage: dbdiff [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      functions
      tables
      tablesrowcount

NB Ensure config.ini is in the same folder that the command is run 

## Sample output
* table actor copy exists in database2 but not database1
* table city copy exists in database1 but not database2
```diff
+|table_catalog:dvdrental|table_schema:public|table name:actor_copy|
-|table_catalog:dvdrental|table_schema:public|table name:city_copy|
```
## Enhancements
* Show differences in table columns
* Show differences in views
* Output queries to json rather than / in addition to dict for debugging purposes
* Filter out 'expected' differences
* Show differences in table data (pygeodiff?)
* Differences in function code
* Trigger differences
* Event trigger differences
* Index and constraint differences
* Iterate through all databases on cluster
* Provide database stats, e.g. schema count and table count
* Make use of click.echo

## Running the tests

    python -m unittest

from this folder

## Using local docker instances for testing
* Install docker compose
* Navigate to the pg9 or pg15 folder
````
docker-compose up
````
* postgres will be accessible on the port mentioned in the docker compose file
````
ports:
  - 5436:5432
````
* Port access will be on 5436 in the above case

## Load data into docker instance

get the sample database:

e.g.
````
wget https://github.com/robconery/dvdrental/archive/master.zip

unzip master
````

restore the data to the docker instance

create dvdrental database in the docker instance

    create database dvdrental

run the script to restore from the sample database in the docker instance

    ./restore.sh dvdrental-master/dvdrental.tar




