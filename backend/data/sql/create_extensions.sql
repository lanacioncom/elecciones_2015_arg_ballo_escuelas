--EXTENSIONS

-- Extension: pg_trgm
-- DROP EXTENSION pg_trgm;
 CREATE EXTENSION IF NOT EXISTS pg_trgm
  SCHEMA public
  VERSION "1.1";

-- Extension: plpgsql
-- DROP EXTENSION plpgsql;
 CREATE EXTENSION IF NOT EXISTS plpgsql
  SCHEMA pg_catalog
  VERSION "1.0";

-- Extension: postgis
-- DROP EXTENSION postgis;
 CREATE EXTENSION IF NOT EXISTS postgis
  SCHEMA public
  VERSION "2.1.7";