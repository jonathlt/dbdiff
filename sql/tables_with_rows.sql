DROP FUNCTION IF EXISTS pg_temp.create_table_list();
CREATE OR REPLACE FUNCTION pg_temp.create_table_list()
  RETURNS TABLE(table_catalog text, table_schema text, table_name text, rowcount bigint)
  LANGUAGE plpgsql AS
$func$
DECLARE
   formal_table text;
   sql_create_table text;
   sql_update_table text;
   sql_result text;
   result_row record;
BEGIN
   EXECUTE 'DROP TABLE IF EXISTS table_list';
   sql_create_table := 'CREATE TEMPORARY TABLE table_list AS  
   						 SELECT table_catalog::text, table_schema::text, table_name::text, 0::bigint as rowcount 
						FROM information_schema.tables where table_schema not in (''pg_catalog'',''information_schema'') and table_type = ''BASE TABLE''';
   EXECUTE sql_create_table;
   FOR result_row IN SELECT * FROM table_list LOOP 
      sql_update_table := 'UPDATE table_list SET rowcount = (SELECT COUNT(*) FROM ' || result_row.table_schema || '.' || result_row.table_name || ')' 
	  	|| ' WHERE table_name = ''' || result_row.table_name || ''' AND table_schema = ''' || result_row.table_schema || '''';

	  RAISE NOTICE 'sql_update_table: %', sql_update_table;
	  EXECUTE sql_update_table;

   END LOOP;
   sql_result := 'SELECT table_catalog, table_schema, table_name, rowcount FROM table_list';
   RETURN QUERY EXECUTE sql_result;
END
$func$;

SELECT * FROM pg_temp.create_table_list();