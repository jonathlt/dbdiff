select table_schema, table_name from information_schema.tables 
where table_schema not in ('pg_catalog','information_schema')
and table_type = 'BASE TABLE';