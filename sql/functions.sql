select distinct routine_catalog, routine_schema, routine_name, pg_get_function_identity_arguments(p.oid) AS arguments_accepted 
from information_schema.routines r, pg_proc p
where r.routine_schema not in ('information_schema','pg_catalog')
and p.proname = r.routine_name;
