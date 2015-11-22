-- Table: hexagons
DROP TABLE IF EXISTS hexagonos;
CREATE TABLE hexagonos
(
  id_hexagono serial,
  wkb_geometry_3857 geometry(Polygon,3857),
  zoom_level integer,
  hex_size double precision,
  num_loc integer,
  arr_loc integer[],
  CONSTRAINT hexagons_pkey PRIMARY KEY (id_hexagono)
)
WITH (
  OIDS=FALSE
);

-- Index: hexagonos_ix_arr
DROP INDEX IF EXISTS hexagonos_ix_arr;

CREATE INDEX hexagonos_ix_arr
  ON hexagonos
  USING GIN
  (arr_loc);

-- Index: hexagonos_ix_geo
DROP INDEX IF EXISTS hexagonos_ix_geo;

CREATE INDEX hexagonos_ix_geo
  ON hexagonos
  USING GIST
  (wkb_geometry_3857);

-- Table: ballo_totales_hexagonos
DROP TABLE IF EXISTS ballo_totales_hexagonos;
CREATE TABLE ballo_totales_hexagonos
(
  id_hexagono serial,
  electores integer,
  votantes integer,
  validos integer,
  positivos integer,
  blancos integer,
  nulos integer,
  CONSTRAINT ballo_totales_hexagonos_pkey PRIMARY KEY (id_hexagono)
)
WITH (
  OIDS=FALSE
);

-- Table: pv_totales_hexagonos
DROP TABLE IF EXISTS pv_totales_hexagonos;
CREATE TABLE pv_totales_hexagonos
(
  id_hexagono serial,
  electores integer,
  votantes integer,
  validos integer,
  positivos integer,
  blancos integer,
  nulos integer,
  CONSTRAINT pv_totales_hexagonos_pkey PRIMARY KEY (id_hexagono)
)
WITH (
  OIDS=FALSE
);

-- Table: paso_totales_hexagonos
DROP TABLE IF EXISTS paso_totales_hexagonos;
CREATE TABLE paso_totales_hexagonos
(
  id_hexagono serial,
  electores integer,
  votantes integer,
  validos integer,
  positivos integer,
  blancos integer,
  nulos integer,
  CONSTRAINT paso_totales_hexagonos_pkey PRIMARY KEY (id_hexagono)
)
WITH (
  OIDS=FALSE
);

-- Table: cache_hexagonos_totales
DROP TABLE IF EXISTS cache_hexagonos_totales;
CREATE TABLE cache_hexagonos_totales
(
  id_hexagono serial,
  wkb_geometry_3857 geometry(Polygon,3857),
  zoom_level integer,
  hex_size double precision,
  num_loc integer,
  localizaciones text,
  electores integer,
  votantes integer,
  validos integer,
  positivos integer,
  blancos integer,
  nulos integer,
  CONSTRAINT cache_hexagonos_totales_pkey PRIMARY KEY (id_hexagono)
)
WITH (
  OIDS=FALSE
);

-- Index: cache_hexagonos_totales_ix_geo
DROP INDEX IF EXISTS cache_hexagonos_totales_ix_geo;

CREATE INDEX cache_hexagonos_totales_ix_geo
  ON cache_hexagonos_totales
  USING GIST
  (wkb_geometry_3857);


-- Table: ballo_resultados_hexagonos
DROP TABLE IF EXISTS ballo_resultados_hexagonos;
CREATE TABLE ballo_resultados_hexagonos
(
  id_hexagono integer,
  id_partido character varying(4),
  agg_pos integer,
  agg_votos integer,
  agg_porc double precision,
  CONSTRAINT ballo_resultados_hexagonos_pkey PRIMARY KEY (id_hexagono, id_partido)
)
WITH (
  OIDS=FALSE
);

-- Table: cache_ballo_winner_hexagonos
DROP TABLE IF EXISTS cache_ballo_winner_hexagonos;
CREATE TABLE cache_ballo_winner_hexagonos
(
  id_hexagono integer,
  wkb_geometry_3857 geometry(Polygon,3857),
  zoom_level integer,
  hex_size double precision,
  num_loc integer,
  electores integer,
  positivos integer,
  votantes integer,
  id_partido character varying(4),
  votos integer,
  margin_victory integer,
  CONSTRAINT cache_ballo_winner_hexagonos_pkey PRIMARY KEY (id_hexagono)
)
WITH (
  OIDS=FALSE
);

-- Table: cache_ballo_resultados_hexagonos
DROP TABLE IF EXISTS cache_ballo_resultados_hexagonos;
CREATE TABLE cache_ballo_resultados_hexagonos
(
  id_hexagono integer,
  id_partido character varying(4),
  winner integer DEFAULT 0,
  swing integer DEFAULT 0, 
  agg_pos integer,
  agg_pos_pv integer,
  agg_pos_paso integer,
  agg_votos integer,
  agg_votos_pv integer,
  agg_votos_paso integer,
  agg_porc double precision,
  agg_porc_pv double precision,
  agg_porc_paso double precision,
  CONSTRAINT cache_ballo_resultados_hexagonos_pkey PRIMARY KEY (id_hexagono, id_partido)
)
WITH (
  OIDS=FALSE
);

-- Table: pv_resultados_hexagonos
DROP TABLE IF EXISTS pv_resultados_hexagonos;
CREATE TABLE pv_resultados_hexagonos
(
  id_hexagono integer,
  id_partido character varying(4),
  agg_pos integer,
  agg_votos integer,
  agg_porc double precision,
  CONSTRAINT pv_resultados_hexagonos_pkey PRIMARY KEY (id_hexagono, id_partido)
)
WITH (
  OIDS=FALSE
);

-- Table: cache_pv_winner_hexagonos
DROP TABLE IF EXISTS cache_pv_winner_hexagonos;
CREATE TABLE cache_pv_winner_hexagonos
(
  id_hexagono integer,
  wkb_geometry_3857 geometry(Polygon,3857),
  zoom_level integer,
  hex_size double precision,
  num_loc integer,
  electores integer,
  positivos integer,
  votantes integer,
  id_partido character varying(4),
  votos integer,
  margin_victory integer,
  CONSTRAINT cache_pv_winner_hexagonos_pkey PRIMARY KEY (id_hexagono)
)
WITH (
  OIDS=FALSE
);

-- Table: cache_pv_resultados_hexagonos
DROP TABLE IF EXISTS cache_pv_resultados_hexagonos;
CREATE TABLE cache_pv_resultados_hexagonos
(
  id_hexagono integer,
  id_partido character varying(4),
  winner integer DEFAULT 0,
  swing integer DEFAULT 0,
  agg_pos integer,
  agg_pos_paso integer,
  agg_votos integer,
  agg_votos_paso integer,
  agg_porc double precision,
  agg_porc_paso double precision,
  CONSTRAINT cache_pv_resultados_hexagonos_pkey PRIMARY KEY (id_hexagono, id_partido)
)
WITH (
  OIDS=FALSE
);

-- Table: paso_resultados_hexagonos
DROP TABLE IF EXISTS paso_resultados_hexagonos;
CREATE TABLE paso_resultados_hexagonos
(
  id_hexagono integer,
  id_partido character varying(4),
  agg_pos double precision,
  agg_votos integer,
  agg_porc double precision,
  CONSTRAINT paso_resultados_hexagonos_pkey PRIMARY KEY (id_hexagono, id_partido)
)
WITH (
  OIDS=FALSE
);

-- Table: cache_paso_resultados_hexagonos
DROP TABLE IF EXISTS cache_paso_resultados_hexagonos;
CREATE TABLE cache_paso_resultados_hexagonos
(
  id_hexagono integer,
  id_partido character varying(4),
  winner integer DEFAULT 0,
  swing integer DEFAULT 0,
  agg_pos double precision,
  agg_votos integer,
  agg_porc double precision,
  CONSTRAINT cache_paso_resultados_hexagonos_pkey PRIMARY KEY (id_hexagono, id_partido)
)
WITH (
  OIDS=FALSE
);

-- Table: cache_paso_winner_hexagonos
DROP TABLE IF EXISTS cache_paso_winner_hexagonos;
CREATE TABLE cache_paso_winner_hexagonos
(
  id_hexagono integer,
  wkb_geometry_3857 geometry(Polygon,3857),
  zoom_level integer,
  hex_size double precision,
  num_loc integer,
  electores integer,
  positivos integer,
  votantes integer,
  id_partido character varying(4),
  votos integer,
  margin_victory integer,
  CONSTRAINT cache_paso_winner_hexagonos_pkey PRIMARY KEY (id_hexagono)
)
WITH (
  OIDS=FALSE
);

