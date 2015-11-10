# coding: utf-8
import dataset
import os
from time import time
from settings import DATABASE_URL, DATABASE_TYPES

# GLOBAL SETTINGS
db = None


def create_polling_relations():
    '''create temp table'''
    q = '''
        SELECT e.id_establecimiento,
               r.id_agrupado,
               e.key_sie,
               e.id_distrito,
               e.distrito,
               e.id_seccion,
               e.seccion,
               e.nombre,
               e.direccion,
               e.localidad,
               e.cod_postal,
               e.id_circuito,
               e.num_mesas,
               (e.mesa_desde || '-' || e.mesa_hasta) as rango,
               e.wkb_geometry_4326
        FROM establecimientos e, relaciones r
        WHERE e.id_establecimiento = r.id_establecimiento
    '''
    results = db.query(q)
    t = db.create_table('establecimientos_tmp',
                        primary_id='id_establecimiento',
                        primary_type='Integer')
    t.create_index(['id_agrupado'], name='ix_id_agrupado')
    t.insert_many(results,
                  chunk_size=1000,
                  types=DATABASE_TYPES)


def create_location_telegrams():
    '''create temp table'''
    q = '''
        SELECT r.id_agrupado,
               e.key_telegrama
        FROM establecimientos_mesas e, relaciones r
        WHERE e.id_establecimiento = r.id_establecimiento
        ORDER BY r.id_agrupado
    '''
    results = db.query(q)
    t = db.create_table('localizaciones_telegramas')
    t.create_index(['id_agrupado'], name='ix_id_agrupado')
    t.insert_many(results,
                  chunk_size=1000,
                  types=DATABASE_TYPES)


def create_locations():
    '''create polling stations by location'''
    q = '''
        WITH agg as (SELECT id_agrupado, SUM(num_mesas) as num_mesas,
                     array_to_string(array_agg(rango), ',') as rangos_mesas,
                     array_to_string(array_agg(id_circuito), ',') as circuitos,
                     array_to_string(array_agg(id_establecimiento), ',') as establecimientos,
                     array_to_string(array_agg(key_sie), ',') as keys_sie
                     FROM establecimientos_tmp
                     GROUP BY id_agrupado),
             loc as (SELECT t1.*
                     FROM establecimientos_tmp as t1
                     LEFT OUTER JOIN establecimientos_tmp as t2
                     ON t1.id_agrupado = t2.id_agrupado
                     AND t1.id_establecimiento > t2.id_establecimiento
                    WHERE t2.id_agrupado IS NULL)
        SELECT l.id_agrupado,
               l.id_distrito,
               l.distrito,
               l.id_seccion,
               l.seccion,
               l.nombre,
               l.direccion,
               l.localidad,
               l.cod_postal,
               a.num_mesas, a.rangos_mesas,
               a.circuitos,
               a.establecimientos, a.keys_sie,
               l.wkb_geometry_4326
        FROM loc l, agg a
        WHERE l.id_agrupado = a.id_agrupado
    '''
    results = db.query(q)
    t = db.create_table('localizaciones',
                        primary_id='id_agrupado',
                        primary_type='Integer')
    t.insert_many(results,
                  chunk_size=1000,
                  types=DATABASE_TYPES)


def aggregate_totals_by_poll_station(elec='paso'):
    ''' aggregate totals by polling station'''
    db_preffix = elec
    src_table = '%s_totales_mesas' % (db_preffix)
    q = '''
        SELECT e.id_establecimiento, e.key_sie,
               SUM(t.electores) as electores,
               SUM(t.votantes) as votantes,
               SUM(t.validos) as validos,
               SUM(t.positivos) as positivos,
               SUM(t.blancos) as blancos,
               SUM(t.nulos) as nulos,
               COUNT(e.id_establecimiento) as num_mesas
        FROM establecimientos_mesas e, %s t
        WHERE e.key_wo_circ = t.key_wo_circ
        GROUP BY e.id_establecimiento, e.key_sie;
    ''' % (src_table)

    results = db.query(q)
    t = db.create_table('%s_totales_establecimientos' % (db_preffix),
                        primary_id='id_establecimiento',
                        primary_type='Integer')
    t.create_index(['key_sie'], name='ix_sie')
    t.insert_many(results,
                  chunk_size=1000,
                  types=DATABASE_TYPES)


def aggregate_results_by_poll_station_by_party(elec='paso'):
    ''' aggregate results by polling station'''
    db_preffix = elec
    src_table = '%s_resultados_mesas' % (db_preffix)
    q = '''
        SELECT e.id_establecimiento,
               e.key_sie,
               r.id_partido,
               SUM(r.votos) as votos
        FROM establecimientos_mesas e, partidos p, %s r
        WHERE e.key_wo_circ = r.key_wo_circ
        AND r.id_partido = p.id_partido
        GROUP BY e.id_establecimiento, e.key_sie, r.id_partido
        ORDER BY e.id_establecimiento;
    ''' % (src_table)

    results = db.query(q)
    t = db.create_table('%s_resultados_establecimientos' % (db_preffix))
    t.create_index(['key_sie'], name='ix_sie')
    t.create_index(['id_partido'], name='ix_party')
    t.insert_many(results,
                  chunk_size=5000,
                  types=DATABASE_TYPES)


def aggregate_totals_by_location(elec='paso'):
    ''' aggregate totals by location'''
    db_preffix = elec
    src_table = '%s_totales_establecimientos' % (db_preffix)
    q = '''
        SELECT l.id_agrupado,
               SUM(t.electores) as electores,
               SUM(t.votantes) as votantes,
               SUM(t.validos) as validos,
               SUM(t.positivos) as positivos,
               SUM(t.blancos) as blancos,
               SUM(t.nulos) as nulos,
               SUM(t.num_mesas) as num_mesas
        FROM relaciones l, %s t
        WHERE l.id_establecimiento = t.id_establecimiento
        GROUP BY l.id_agrupado;
    ''' % (src_table)

    results = db.query(q)
    t = db.create_table('%s_totales_localizaciones' % (db_preffix),
                        primary_id='id_agrupado',
                        primary_type='Integer')
    t.insert_many(results,
                  chunk_size=1000,
                  types=DATABASE_TYPES)


def aggregate_results_by_location_by_party(elec='paso'):
    ''' aggregate results by location and party'''
    db_preffix = elec
    src_table = '%s_resultados_establecimientos' % (db_preffix)
    q = '''
        SELECT l.id_agrupado,
               r.id_partido,
               SUM(r.votos) as votos
        FROM relaciones l, %s r
        WHERE l.id_establecimiento = r.id_establecimiento
        GROUP BY l.id_agrupado, r.id_partido
        ORDER BY l.id_agrupado;
    ''' % (src_table)

    results = db.query(q)
    t = db.create_table('%s_resultados_localizaciones' % (db_preffix))
    t.create_index(['id_partido'], name='ix_party')
    t.insert_many(results,
                  chunk_size=5000,
                  types=DATABASE_TYPES)


def create_winner_table(elec='paso', loc=False):
    '''create winner table using postgres window sugar'''
    extra_columns_loc = 's.num_mesas, s.rangos_mesas, \
                         s.circuitos, s.keys_sie, s.establecimientos,'
    extra_columns_est = 's.key_sie, s.id_circuito, \
                         s.num_mesas, s.mesa_desde, s.mesa_hasta,'

    db_preffix = elec
    src = 'localizaciones' if loc else 'establecimientos'
    key = 'id_agrupado' if loc else 'id_establecimiento'
    extra_columns = extra_columns_loc if loc else extra_columns_est
    r_table = '%s_resultados_%s' % (db_preffix, src)
    t_table = '%s_totales_%s' % (db_preffix, src)
    q = '''
        WITH winner AS (SELECT %(key)s, id_partido, votos,
                            row_number() over(partition by %(key)s
                                ORDER BY votos DESC) as rank,
                            (votos - lead(votos,1,0) over(partition by %(key)s
                                ORDER BY votos DESC)) as margin_victory
                        FROM %(results)s
                        ORDER BY %(key)s, rank)
        SELECT s.%(key)s,
               %(extra)s
               s.id_distrito, s.distrito,
               s.id_seccion, s.seccion,
               s.nombre, s.direccion,
               s.localidad, s.cod_postal,
               s.wkb_geometry_4326 as geom,
               t.electores, t.positivos,
               t.votantes, sqrt(t.positivos) as sqrt_positivos,
               w.id_partido, w.votos, w.margin_victory
        FROM %(src)s s, winner w, %(totals)s t
        WHERE s.%(key)s = w.%(key)s
        AND s.%(key)s = t.%(key)s
        AND w.rank = 1;
    ''' % {'results': r_table, 'totals': t_table, 'key': key,
           'src': src, 'extra': extra_columns}
    (r_table, 'establecimientos', t_table)

    results = db.query(q)
    t = db.create_table('%s_winner_%s' % (db_preffix, src),
                        primary_id=key,
                        primary_type='Integer')
    t.insert_many(results, chunk_size=1000, types=DATABASE_TYPES)


def create_diff_table(loc=False):
    '''get the difference for each polling station
       and party between past and actual elections'''
    src = 'localizaciones' if loc else 'establecimientos'
    key = 'id_agrupado' if loc else 'id_establecimiento'

    q = '''
        SELECT r.%(key)s,
               r.id_partido,
               r.votos as votos,
               rpv.votos as votos_pv,
               rp.votos as votos_paso,
               (r.votos - rp.votos) as dif_paso,
               (r.votos - rpv.votos) as dif_pv
        FROM ballo_resultados_%(src)s r,
             pv_resultados_%(src)s rpv,
             paso_resultados_%(src)s rp
        WHERE r.%(key)s = rp.%(key)s
        AND r.id_partido = rp.id_partido
        AND r.%(key)s = rpv.%(key)s
        AND r.id_partido = rpv.id_partido
    ''' % {'key': key, 'src': src}

    results = db.query(q)
    t = db.create_table('ballo_diff_%s' % (src))
    t.create_index(['id_partido'], name='ix_party')
    t.create_index([key], name='ix_poll')
    t.insert_many(results, chunk_size=5000, types=DATABASE_TYPES)


def create_polling_geo_w_totals(loc=False):
    '''get the denormalized totals table'''
    src = 'localizaciones' if loc else 'establecimientos'
    key = 'id_agrupado' if loc else 'id_establecimiento'

    q = '''
        SELECT s.*,
               t.electores,
               t.votantes,
               t.validos,
               t.positivos,
               t.blancos,
               t.nulos
        FROM %(src)s s,
             pv_totales_%(src)s t
        WHERE s.%(key)s = t.%(key)s
    ''' % {'key': key, 'src': src}

    results = db.query(q)
    t = db.create_table('%s_totales' % (src),
                        primary_id=key,
                        primary_type='Integer')
    t.insert_many(results, chunk_size=1000, types=DATABASE_TYPES)


def run():
    '''process elections data'''
    start_time = time()
    print "create location tables"
    create_location_tables()
    print "Aggregate data for paso elections"
    process_data(elec='paso')
    print "process paso data: %s seconds" % (time() - start_time)
    print "Aggregate data for pv elections"
    process_data(elec='pv')
    print "process pv data: %s seconds" % (time() - start_time)
    print "Aggregate data for ballottage elections"
    process_data(elec='ballo')
    print "process ballo data: %s seconds" % (time() - start_time)
    print "Create cartodb tables"
    create_cartodb()
    print "create_cartodb: %s seconds" % (time() - start_time)


def create_location_tables():
    '''create location tables for the elections'''
    print "create temp polling station table"
    create_polling_relations()

    print "deduplicate location table"
    create_locations()

    print "create shortcut table for telegram access"
    create_location_telegrams()


def process_data(elec='paso'):
    '''process data from an election'''
    label = elec
    print "%s: aggregate totals by polling station" % (label)
    aggregate_totals_by_poll_station(elec=elec)

    print "%s: aggregate results by polling station and party" % (label)
    aggregate_results_by_poll_station_by_party(elec=elec)

    print "%s: aggregate totals by location" % (label)
    aggregate_totals_by_location(elec=elec)

    print "%s: aggregate results by location and party" % (label)
    aggregate_results_by_location_by_party(elec=elec)


def create_cartodb():
    print "create polling station paso winner"
    create_winner_table(elec='paso')
    print "create location paso winner"
    create_winner_table(elec='paso', loc=True)

    print "create polling station pv winner"
    create_winner_table(elec='pv', loc=False)
    print "create location pv winner"
    create_winner_table(elec='pv', loc=True)

    print "create polling station ballottage winner"
    create_winner_table(elec='ballo', loc=False)
    print "create location ballottage winner"
    create_winner_table(elec='ballo', loc=True)

    print "create polling station differences"
    create_diff_table()
    print "create location differences"
    create_diff_table(loc=True)

    print "create polling stations with totals"
    create_polling_geo_w_totals()
    print "create location with totals"
    create_polling_geo_w_totals(loc=True)


if __name__ == "__main__":
    db = dataset.connect(DATABASE_URL)
    run()
