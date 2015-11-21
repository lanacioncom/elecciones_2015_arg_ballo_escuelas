-- Index: localizaciones_ix_geo
DROP INDEX IF EXISTS localizaciones_ix_geo;

CREATE INDEX localizaciones_ix_geo
  ON localizaciones
  USING GIST
  (wkb_geometry_4326);

-- Index: localizaciones_ix_geo
DROP INDEX IF EXISTS localizaciones_ix_mercator;

CREATE INDEX localizaciones_ix_mercator
  ON localizaciones
  USING GIST
  (wkb_geometry_3857);

-- Index: ballo_resultados_localizaciones_ix_agrupado
DROP INDEX IF EXISTS ballo_resultados_localizaciones_ix_agrupado;

CREATE INDEX ballo_resultados_localizaciones_ix_agrupado
  ON ballo_resultados_localizaciones
  USING BTREE
  (id_agrupado);

-- Index: ballo_resultados_localizaciones_ix_partido
DROP INDEX IF EXISTS ballo_resultados_localizaciones_ix_partido;

CREATE INDEX ballo_resultados_localizaciones_ix_partido
  ON ballo_resultados_localizaciones
  USING BTREE
  (id_partido);

-- Index: pv_resultados_localizaciones_ix_agrupado
DROP INDEX IF EXISTS pv_resultados_localizaciones_ix_agrupado;

CREATE INDEX pv_resultados_localizaciones_ix_agrupado
  ON pv_resultados_localizaciones
  USING BTREE
  (id_agrupado);

-- Index: pv_resultados_localizaciones_ix_partido
DROP INDEX IF EXISTS pv_resultados_localizaciones_ix_partido;

CREATE INDEX pv_resultados_localizaciones_ix_partido
  ON pv_resultados_localizaciones
  USING BTREE
  (id_partido);

-- Index: paso_resultados_localizaciones_ix_agrupado
DROP INDEX IF EXISTS paso_resultados_localizaciones_ix_agrupado;

CREATE INDEX paso_resultados_localizaciones_ix_agrupado
  ON paso_resultados_localizaciones
  USING BTREE
  (id_agrupado);

-- Index: paso_resultados_localizaciones_ix_partido
DROP INDEX IF EXISTS paso_resultados_localizaciones_ix_partido;

CREATE INDEX paso_resultados_localizaciones_ix_partido
  ON paso_resultados_localizaciones
  USING BTREE
  (id_partido);

-- Index: ballo_totales_localizaciones_ix_agrupado
DROP INDEX IF EXISTS ballo_totales_localizaciones_ix_agrupado;

CREATE INDEX ballo_totales_localizaciones_ix_agrupado
  ON ballo_totales_localizaciones
  USING BTREE
  (id_agrupado);

-- Index: pv_totales_localizaciones_ix_agrupado
DROP INDEX IF EXISTS pv_totales_localizaciones_ix_agrupado;

CREATE INDEX pv_totales_localizaciones_ix_agrupado
  ON pv_totales_localizaciones
  USING BTREE
  (id_agrupado);

-- Index: paso_totales_localizaciones_ix_agrupado
DROP INDEX IF EXISTS paso_totales_localizaciones_ix_agrupado;

CREATE INDEX paso_totales_localizaciones_ix_agrupado
  ON paso_totales_localizaciones
  USING BTREE
  (id_agrupado);