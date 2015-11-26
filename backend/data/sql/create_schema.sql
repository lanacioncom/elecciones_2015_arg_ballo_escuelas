--TABLES AND INDEXES

-- Table: establecimientos
DROP TABLE IF EXISTS establecimientos;
CREATE TABLE establecimientos
(
  id_establecimiento integer NOT NULL,
  key_sie character varying(12) NOT NULL,
  id_distrito character varying(2) NOT NULL,
  distrito character varying(50),
  id_seccion character varying(3) NOT NULL,
  seccion character varying(100),
  id_circuito character varying(5) NOT NULL,
  nombre character varying(200),
  direccion character varying(200),
  localidad character varying(100),
  cod_postal character varying(20),
  mesa_desde character varying(4),
  mesa_hasta character varying(4),
  num_mesas integer,
  mesa_desde_inun character varying(4),
  mesa_hasta_inun character varying(4),
  latitud double precision,
  longitud double precision,
  wkb_geometry_4326 geometry(Point,4326),
  CONSTRAINT establecimientos_pkey PRIMARY KEY (id_establecimiento)
)
WITH (
  OIDS=FALSE
);

-- Index: establecimientos_ix_sie
DROP INDEX IF EXISTS establecimientos_ix_sie;

CREATE INDEX establecimientos_ix_sie
  ON establecimientos
  USING btree
  (key_sie);


-- Index: establecimientos_ix_geo
DROP INDEX IF EXISTS establecimientos_ix_geo;

CREATE INDEX establecimientos_ix_geo
  ON establecimientos
  USING GIST
  (wkb_geometry_4326);


-- Table: ambitos
DROP TABLE IF EXISTS ambitos;
CREATE TABLE ambitos
(
  id serial NOT NULL,
  id_distrito character varying(2),
  distrito character varying(50),
  id_seccion character varying(3),
  seccion character varying(100),
  CONSTRAINT ambitos_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);


-- Table: establecimientos_mesas
DROP TABLE IF EXISTS establecimientos_mesas;
CREATE TABLE establecimientos_mesas
(
  id_establecimiento integer,
  key_sie character varying(12),
  key_circ character varying(17),
  key_wo_circ character varying(11) NOT NULL,
  id_distrito character varying(2),
  id_seccion character varying(3),
  id_circuito character varying(5),
  id_mesa character varying(4),
  key_telegrama character varying(27),
  CONSTRAINT establecimientos_mesas_pkey PRIMARY KEY (key_wo_circ)
)
WITH (
  OIDS=FALSE
);

-- Index: establecimientos_mesas_ix_poll
DROP INDEX IF EXISTS establecimientos_mesas_ix_poll;
CREATE INDEX establecimientos_mesas_ix_poll
  ON establecimientos_mesas
  USING btree
  (id_establecimiento);


-- Table: establecimientos
DROP TABLE IF EXISTS relaciones;
CREATE TABLE relaciones
(
  id_establecimiento integer NOT NULL,
  id_agrupado integer NOT NULL,
  CONSTRAINT relaciones_pkey PRIMARY KEY (id_establecimiento)
)
WITH (
  OIDS=FALSE
);

-- Index: establecimientos_ix_sie
DROP INDEX IF EXISTS relaciones_ix_agrupado;

CREATE INDEX relaciones_ix_agrupado
  ON relaciones
  USING btree
  (id_agrupado);


-- Table: partidos
DROP TABLE IF EXISTS partidos;
CREATE TABLE partidos
(
  id_partido character varying(4) NOT NULL,
  siglas character varying(50),
  nombre character varying(200),
  CONSTRAINT partidos_pkey PRIMARY KEY (id_partido)
)
WITH (
  OIDS=FALSE
);

-- Table: paso_totales_mesa
DROP TABLE IF EXISTS paso_totales_mesas;
CREATE TABLE paso_totales_mesas
(
  key_circ character varying(17),
  key_wo_circ character varying(11) NOT NULL,
  id_distrito character varying(2),
  id_seccion character varying(3),
  id_circuito character varying(5),
  id_mesa character varying(4),
  electores integer,
  votantes integer,
  validos integer,
  positivos integer,
  blancos integer,
  nulos integer,
  CONSTRAINT paso_totales_mesas_pkey PRIMARY KEY (key_wo_circ)
)
WITH (
  OIDS=FALSE
);

-- Table: paso_resultados_mesa
DROP TABLE IF EXISTS paso_resultados_mesas;
CREATE TABLE paso_resultados_mesas
(
  id serial NOT NULL,
  key_circ character varying(17),
  key_wo_circ character varying(11),
  id_distrito character varying(2),
  id_seccion character varying(3),
  id_circuito character varying(5),
  id_mesa character varying(4),
  id_partido character varying(4),
  votos integer,
  CONSTRAINT paso_resultados_mesas_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);

-- Table: pv_totales_mesa
DROP TABLE IF EXISTS pv_totales_mesas;
CREATE TABLE pv_totales_mesas
(
  key_circ character varying(17),
  key_wo_circ character varying(11) NOT NULL,
  id_distrito character varying(2),
  id_seccion character varying(3),
  id_circuito character varying(5),
  id_mesa character varying(4),
  electores integer,
  votantes integer,
  validos integer,
  positivos integer,
  blancos integer,
  nulos integer,
  CONSTRAINT pv_totales_mesas_pkey PRIMARY KEY (key_wo_circ)
)
WITH (
  OIDS=FALSE
);

-- Table: pv_resultados_mesa
DROP TABLE IF EXISTS pv_resultados_mesas;
CREATE TABLE pv_resultados_mesas
(
  id serial NOT NULL,
  key_circ character varying(17),
  key_wo_circ character varying(11),
  id_distrito character varying(2),
  id_seccion character varying(3),
  id_circuito character varying(5),
  id_mesa character varying(4),
  id_partido character varying(4),
  votos integer,
  CONSTRAINT pv_resultados_mesas_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);

-- Table: ballo_totales_mesa
DROP TABLE IF EXISTS ballo_totales_mesas;
CREATE TABLE ballo_totales_mesas
(
  key_circ character varying(17),
  key_wo_circ character varying(11) NOT NULL,
  id_distrito character varying(2),
  id_seccion character varying(3),
  id_circuito character varying(5),
  id_mesa character varying(4),
  electores integer,
  votantes integer,
  validos integer,
  positivos integer,
  blancos integer,
  nulos integer,
  CONSTRAINT ballo_totales_mesas_pkey PRIMARY KEY (key_wo_circ)
)
WITH (
  OIDS=FALSE
);

-- Table: ballo_resultados_mesa
DROP TABLE IF EXISTS ballo_resultados_mesas;
CREATE TABLE ballo_resultados_mesas
(
  id serial NOT NULL,
  key_circ character varying(17),
  key_wo_circ character varying(11),
  id_distrito character varying(2),
  id_seccion character varying(3),
  id_circuito character varying(5),
  id_mesa character varying(4),
  id_partido character varying(4),
  votos integer,
  CONSTRAINT ballo_resultados_mesas_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);

-- Table: ballo_document_cloud
DROP TABLE IF EXISTS ballo_document_cloud;
CREATE TABLE ballo_document_cloud
(
  id_document character varying(8) NOT NULL,
  title character varying(30),
  id_project character varying(8),
  CONSTRAINT ballo_document_cloud_pkey PRIMARY KEY (id_document)
)
WITH (
  OIDS=FALSE
);

