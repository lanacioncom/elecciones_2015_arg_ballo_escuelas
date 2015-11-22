# coding: utf-8
insert_hex_sql = '''
WITH loc_bbox(bbox) AS (SELECT ST_EXPAND(ST_ENVELOPE(
                                            ST_COLLECT(wkb_geometry_3857)
                                        ),
                                        CDB_XYZ_Resolution(%(z)s) * %(size)s)
                        FROM localizaciones
                        WHERE NOT (id_distrito = '24' AND id_seccion = '003')),
hgrid(cell) AS (SELECT CDB_HexagonGrid(l.bbox,
                                       CDB_XYZ_Resolution(%(z)s) * %(size)s)
                FROM loc_bbox l)
INSERT INTO hexagonos(wkb_geometry_3857,zoom_level,hex_size, num_loc,arr_loc)
SELECT h.cell as wkb_geometry_3857, %(z)s as zoom_level, %(size)s as hex_size,
       COUNT(*) as num_loc, array_agg(l.id_agrupado) as arr_loc
FROM hgrid h, localizaciones l
WHERE ST_INTERSECTS(l.wkb_geometry_3857, h.cell)
GROUP BY h.cell
ORDER BY num_loc desc;
'''

insert_hex_lzoom_sql = '''
WITH hexa(bbox) AS (SELECT ST_EXPAND(ST_ENVELOPE(wkb_geometry_3857),
                    CDB_XYZ_Resolution(%(z)s) * %(size)s)
                    FROM hexagonos WHERE zoom_level = %(zold)s),
hgrid(cell) AS (
    SELECT CDB_HexagonGrid(h.bbox,CDB_XYZ_Resolution(%(z)s) * %(size)s)
    FROM hexa h)
INSERT INTO hexagonos(wkb_geometry_3857,zoom_level,hex_size, num_loc,arr_loc)
SELECT h.cell as wkb_geometry_3857, %(z)s as zoom_level, %(size)s as hex_size,
       COUNT(*) as num_loc, array_agg(l.id_agrupado) as arr_loc
FROM hgrid h, localizaciones l
WHERE ST_INTERSECTS(l.wkb_geometry_3857, h.cell)
GROUP BY h.cell
ORDER BY num_loc desc;
'''

cache_insert_hex_totales_sql = '''
INSERT INTO cache_hexagonos_totales
SELECT h.id_hexagono, h.wkb_geometry_3857,
h.zoom_level, h.hex_size, h.num_loc,
array_to_string(h.arr_loc, ',') as loc_list,
SUM(t.electores) as agg_electores,
SUM(t.votantes) as agg_votantes,
SUM(t.validos) as agg_validos,
SUM(t.positivos) as agg_positivos,
SUM(t.blancos) as agg_blancos,
SUM(t.nulos) as agg_nulos
FROM hexagonos h, ballo_totales_localizaciones t
WHERE t.id_agrupado = ANY(h.arr_loc)
GROUP BY h.id_hexagono
'''

insert_hex_totales_sql = '''
INSERT INTO %(dest)s
SELECT h.id_hexagono,
SUM(t.electores) as agg_electores,
SUM(t.votantes) as agg_votantes,
SUM(t.validos) as agg_validos,
SUM(t.positivos) as agg_positivos,
SUM(t.blancos) as agg_blancos,
SUM(t.nulos) as agg_nulos
FROM hexagonos h, %(totals)s t
WHERE t.id_agrupado = ANY(h.arr_loc)
GROUP BY h.id_hexagono
'''


insert_hex_results_sql = '''
INSERT INTO %(dest)s
SELECT h.id_hexagono, r.id_partido,
SUM(t.positivos) as agg_pos,
SUM(r.votos) as agg_votos,
CASE WHEN SUM(t.positivos) = 0 THEN 0
     ELSE (SUM(r.votos)/SUM(t.positivos)::float)
     END as agg_porc
FROM hexagonos h,
%(results)s r, %(totals)s t
WHERE r.id_agrupado = t.id_agrupado
AND r.id_agrupado = ANY (h.arr_loc)
GROUP BY h.id_hexagono, r.id_partido
ORDER BY id_hexagono, agg_votos desc
'''

cache_insert_ballo_results_hex_sql = '''
INSERT INTO cache_ballo_resultados_hexagonos
SELECT h.id_hexagono, ballo_r.id_partido,
0 as winner,
0 as new,
SUM(ballo_t.positivos) as agg_pos,
SUM(pv_t.positivos) as agg_pos_pv,
SUM(paso_t.positivos) as agg_pos_paso,
SUM(ballo_r.votos) as agg_votos,
SUM(pv_r.votos) as agg_votos_pv,
SUM(paso_r.votos) as agg_votos_paso,
CASE WHEN SUM(ballo_t.positivos) = 0 THEN 0
     ELSE (SUM(ballo_r.votos)/SUM(ballo_t.positivos)::float)
     END as agg_porc,
CASE WHEN SUM(pv_t.positivos) = 0 THEN 0
     ELSE (SUM(pv_r.votos)/SUM(pv_t.positivos)::float)
     END as agg_porc_pv,
CASE WHEN SUM(paso_t.positivos) = 0 THEN 0
     ELSE (SUM(paso_r.votos)/SUM(paso_t.positivos)::float)
     END as agg_porc_paso
FROM hexagonos h,
ballo_resultados_localizaciones ballo_r, ballo_totales_localizaciones ballo_t,
pv_resultados_localizaciones pv_r, pv_totales_localizaciones pv_t,
paso_resultados_localizaciones paso_r, paso_totales_localizaciones paso_t
WHERE ballo_r.id_agrupado = ballo_t.id_agrupado
AND ballo_r.id_agrupado = pv_r.id_agrupado
AND pv_r.id_agrupado = pv_t.id_agrupado
AND ballo_r.id_partido = pv_r.id_partido
AND ballo_r.id_agrupado = paso_r.id_agrupado
AND paso_r.id_agrupado = paso_t.id_agrupado
AND ballo_r.id_partido = paso_r.id_partido
AND ballo_r.id_agrupado = ANY (h.arr_loc)
GROUP BY h.id_hexagono, ballo_r.id_partido
ORDER BY id_hexagono, agg_votos desc
'''

cache_insert_pv_results_hex_sql = '''
INSERT INTO cache_pv_resultados_hexagonos
SELECT h.id_hexagono, pv_r.id_partido,
0 as winner,
0 as new,
SUM(pv_t.positivos) as agg_pos,
SUM(paso_t.positivos) as agg_pos_paso,
SUM(pv_r.votos) as agg_votos,
SUM(paso_r.votos) as agg_votos_paso,
CASE WHEN SUM(pv_t.positivos) = 0 THEN 0
     ELSE (SUM(pv_r.votos)/SUM(pv_t.positivos)::float)
     END as agg_porc,
CASE WHEN SUM(paso_t.positivos) = 0 THEN 0
     ELSE (SUM(paso_r.votos)/SUM(paso_t.positivos)::float)
     END as agg_porc_paso
FROM hexagonos h,
pv_resultados_localizaciones pv_r, pv_totales_localizaciones pv_t,
paso_resultados_localizaciones paso_r, paso_totales_localizaciones paso_t
WHERE pv_r.id_agrupado = pv_t.id_agrupado
AND pv_r.id_agrupado = paso_r.id_agrupado
AND paso_r.id_agrupado = paso_t.id_agrupado
AND pv_r.id_partido = paso_r.id_partido
AND pv_r.id_agrupado = ANY (h.arr_loc)
GROUP BY h.id_hexagono, pv_r.id_partido
ORDER BY id_hexagono, agg_votos desc
'''

cache_insert_paso_results_hex_sql = '''
INSERT INTO cache_paso_resultados_hexagonos
SELECT h.id_hexagono, paso_r.id_partido,
0 as winner,
0 as new,
SUM(paso_t.positivos) as agg_pos,
SUM(paso_r.votos) as agg_votos,
CASE WHEN SUM(paso_t.positivos) = 0 THEN 0
     ELSE (SUM(paso_r.votos)/SUM(paso_t.positivos)::float)
     END as agg_porc
FROM hexagonos h,
paso_resultados_localizaciones paso_r, paso_totales_localizaciones paso_t
WHERE paso_r.id_agrupado = paso_t.id_agrupado
AND paso_r.id_agrupado = ANY (h.arr_loc)
GROUP BY h.id_hexagono, paso_r.id_partido
ORDER BY id_hexagono, agg_votos desc;
'''

insert_winner_hex_sql = '''
WITH winner AS (
    SELECT %(key)s, id_partido, agg_votos,
       row_number() over(partition by %(key)s
                         ORDER BY agg_votos DESC) as rank,
       (agg_votos - lead(agg_votos,1,0) over(partition by %(key)s
                                     ORDER BY agg_votos DESC)) as margin_victory
    FROM %(results)s
    ORDER BY %(key)s, rank)
INSERT INTO %(dest)s
SELECT h.%(key)s,
       h.wkb_geometry_3857,
       h.zoom_level, h.hex_size,
       h.num_loc,
       t.electores, t.positivos, t.votantes,
       w.id_partido, w.agg_votos as votos, w.margin_victory
FROM winner w, %(totals)s t, hexagonos h
WHERE t.%(key)s = w.%(key)s
AND h.%(key)s = w.%(key)s
AND w.rank = 1;
'''

test_hex_sql = '''
WITH loc_bbox(bbox) AS (SELECT ST_EXPAND(ST_ENVELOPE(
                                            ST_COLLECT(wkb_geometry_3857)
                                        ),
                                        CDB_XYZ_Resolution(%(z)s) * %(size)s)
                        FROM localizaciones
                        WHERE NOT (id_distrito = '24' AND id_seccion = '003')),
hgrid(cell) AS (SELECT CDB_HexagonGrid(l.bbox,
                                       CDB_XYZ_Resolution(4) * 30)
                FROM loc_bbox l)
--INSERT INTO hexagonos(wkb_geometry_3857,zoom_level,hex_size, num_loc,arr_loc)
SELECT h.cell as wkb_geometry_3857, 4 as zoom_level, 30 as hex_size,
       COUNT(*) as num_loc, array_agg(l.id_agrupado) as arr_loc
FROM hgrid h, localizaciones l
WHERE ST_INTERSECTS(l.wkb_geometry_3857, h.cell)
GROUP BY h.cell
ORDER BY num_loc desc;
'''

insert_antartida_hex_sql = '''
WITH antartida AS (
    SELECT id_agrupado, wkb_geometry_3857
    FROM localizaciones
    WHERE (id_distrito = '24' AND id_seccion = '003'))
INSERT INTO hexagonos(wkb_geometry_3857,zoom_level,hex_size, num_loc,arr_loc)
SELECT CDB_MakeHexagon(a.wkb_geometry_3857,
                       CDB_XYZ_Resolution(%(z)s) * %(size)s),
%(z)s as zoom_level, %(size)s as hex_size,
1 as num_loc, array[a.id_agrupado]
FROM antartida a
'''

update_cache_set_winner_status = '''
UPDATE %(cache)s r
SET winner = CASE WHEN r.id_partido = w.id_partido THEN 1 ELSE 0 END
FROM %(winner)s w
WHERE r.%(key)s = w.%(key)s
'''

update_cache_set_new_status = '''
UPDATE %(cache)s r
SET new = CASE WHEN (r.id_partido = w.id_partido
                     AND r.id_partido != wprev.id_partido) THEN 1
               WHEN (r.id_partido != w.id_partido
                     AND r.id_partido = wprev.id_partido) THEN 1
               ELSE 0 END
FROM %(winner)s w, %(wprev)s wprev
WHERE r.%(key)s = w.%(key)s
AND r.%(key)s = wprev.%(key)s
'''
