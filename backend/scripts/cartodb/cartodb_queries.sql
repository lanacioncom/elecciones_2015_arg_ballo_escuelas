ALTER TABLE "arg_pv_diff_votos" ALTER COLUMN id_establecimiento TYPE integer USING CAST(CASE id_establecimiento WHEN '' THEN NULL ELSE id_establecimiento END AS INTEGER);
ALTER TABLE "arg_pv_diff_votos" ALTER COLUMN votos TYPE integer USING CAST(CASE votos WHEN '' THEN NULL ELSE votos END AS INTEGER);
ALTER TABLE "arg_pv_diff_votos" ALTER COLUMN votos_paso TYPE integer USING CAST(CASE votos_paso WHEN '' THEN NULL ELSE votos_paso END AS INTEGER);
ALTER TABLE "arg_pv_diff_votos" ALTER COLUMN diferencia TYPE integer USING CAST(CASE diferencia WHEN '' THEN NULL ELSE diferencia END AS INTEGER);
--
ALTER TABLE "arg_pv_establecimientos" ALTER COLUMN id_establecimiento TYPE integer USING CAST(CASE id_establecimiento WHEN '' THEN NULL ELSE id_establecimiento END AS INTEGER);
ALTER TABLE "arg_pv_establecimientos" ALTER COLUMN num_mesas TYPE integer USING CAST(CASE num_mesas WHEN '' THEN NULL ELSE num_mesas END AS INTEGER);
ALTER TABLE "arg_pv_establecimientos" ALTER COLUMN electores TYPE integer USING CAST(CASE electores WHEN '' THEN NULL ELSE electores END AS INTEGER);
ALTER TABLE "arg_pv_establecimientos" ALTER COLUMN votantes TYPE integer USING CAST(CASE votantes WHEN '' THEN NULL ELSE votantes END AS INTEGER);
ALTER TABLE "arg_pv_establecimientos" ALTER COLUMN validos TYPE integer USING CAST(CASE validos WHEN '' THEN NULL ELSE validos END AS INTEGER);
ALTER TABLE "arg_pv_establecimientos" ALTER COLUMN positivos TYPE integer USING CAST(CASE positivos WHEN '' THEN NULL ELSE positivos END AS INTEGER);
ALTER TABLE "arg_pv_establecimientos" ALTER COLUMN blancos TYPE integer USING CAST(CASE blancos WHEN '' THEN NULL ELSE blancos END AS INTEGER);
ALTER TABLE "arg_pv_establecimientos" ALTER COLUMN nulos TYPE integer USING CAST(CASE nulos WHEN '' THEN NULL ELSE nulos END AS INTEGER);
--
ALTER TABLE "arg_paso_ganador" ALTER COLUMN id_establecimiento TYPE integer USING CAST(CASE id_establecimiento WHEN '' THEN NULL ELSE id_establecimiento END AS INTEGER);
ALTER TABLE "arg_paso_ganador" ALTER COLUMN num_mesas TYPE integer USING CAST(CASE num_mesas WHEN '' THEN NULL ELSE num_mesas END AS INTEGER);
ALTER TABLE "arg_paso_ganador" ALTER COLUMN electores TYPE integer USING CAST(CASE electores WHEN '' THEN NULL ELSE electores END AS INTEGER);
ALTER TABLE "arg_paso_ganador" ALTER COLUMN votantes TYPE integer USING CAST(CASE votantes WHEN '' THEN NULL ELSE votantes END AS INTEGER);
ALTER TABLE "arg_paso_ganador" ALTER COLUMN votos TYPE integer USING CAST(CASE votos WHEN '' THEN NULL ELSE votos END AS INTEGER);
ALTER TABLE "arg_paso_ganador" ALTER COLUMN margen_victoria TYPE integer USING CAST(CASE margen_victoria WHEN '' THEN NULL ELSE margen_victoria END AS INTEGER);
ALTER TABLE "arg_paso_ganador" ALTER COLUMN positivos TYPE integer USING CAST(CASE positivos WHEN '' THEN NULL ELSE positivos END AS INTEGER);
ALTER TABLE "arg_paso_ganador" ALTER COLUMN raiz_positivos TYPE double precision USING CAST(CASE raiz_positivos WHEN '' THEN NULL ELSE raiz_positivos END AS DOUBLE PRECISION);
--
ALTER TABLE "arg_pv_ganador" ALTER COLUMN id_establecimiento TYPE integer USING CAST(CASE id_establecimiento WHEN '' THEN NULL ELSE id_establecimiento END AS INTEGER);
ALTER TABLE "arg_pv_ganador" ALTER COLUMN num_mesas TYPE integer USING CAST(CASE num_mesas WHEN '' THEN NULL ELSE num_mesas END AS INTEGER);
ALTER TABLE "arg_pv_ganador" ALTER COLUMN electores TYPE integer USING CAST(CASE electores WHEN '' THEN NULL ELSE electores END AS INTEGER);
ALTER TABLE "arg_pv_ganador" ALTER COLUMN votantes TYPE integer USING CAST(CASE votantes WHEN '' THEN NULL ELSE votantes END AS INTEGER);
ALTER TABLE "arg_pv_ganador" ALTER COLUMN votos TYPE integer USING CAST(CASE votos WHEN '' THEN NULL ELSE votos END AS INTEGER);
ALTER TABLE "arg_pv_ganador" ALTER COLUMN margen_victoria TYPE integer USING CAST(CASE margen_victoria WHEN '' THEN NULL ELSE margen_victoria END AS INTEGER);
ALTER TABLE "arg_pv_ganador" ALTER COLUMN positivos TYPE integer USING CAST(CASE positivos WHEN '' THEN NULL ELSE positivos END AS INTEGER);
ALTER TABLE "arg_pv_ganador" ALTER COLUMN raiz_positivos TYPE double precision USING CAST(CASE raiz_positivos WHEN '' THEN NULL ELSE raiz_positivos END AS DOUBLE PRECISION);
--
ALTER TABLE arg_pv_loc_ganador ADD COLUMN tsv tsvector;
CREATE INDEX arg_pv_loc_ganador_tsv_idx ON arg_pv_loc_ganador USING gin(tsv);
UPDATE arg_pv_loc_ganador SET 
   tsv = setweight(to_tsvector('pg_catalog.spanish', coalesce(nombre,'')), 'A') || 
         setweight(to_tsvector('pg_catalog.spanish', coalesce(direccion,'')), 'B') ||
         setweight(to_tsvector('pg_catalog.spanish', coalesce(localidad,'')), 'C') ||
         setweight(to_tsvector('pg_catalog.spanish', coalesce(seccion,'')), 'D');
