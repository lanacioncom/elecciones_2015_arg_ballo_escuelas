# coding: utf-8
import argparse
import os
import psycopg2
from time import time
from settings import DATABASE_URL
from lqueries import update_cache_set_winner_status
from lqueries import update_cache_set_new_status

elec_arr = ['paso', 'pv', 'ballo']


def process_winner(elec):
    '''calculate results for all hex levels'''
    print "calculate results for all hex levels"
    template = insert_winner_hex_sql
    key = 'id_hexagono'
    election = elec_arr[elec]
    r_table = '%s_resultados_hexagonos' % (election)
    t_table = '%s_totales_hexagonos' % (election)
    w_table = 'cache_%s_winner_hexagonos' % (election)
    query = template % {'results': r_table, 'totals': t_table,
                        'dest': w_table, 'key': key}
    print query
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    try:
        cur.execute(query)
    except psycopg2.Error, e:
        print e.pgerror
    conn.commit()


def process_winner_status(elec, hexa):
    '''process cache winner status'''
    template = update_cache_set_winner_status
    election = elec_arr[elec]
    key = 'id_hexagono' if hexa else 'id_agrupado'
    suffix = 'hexagonos' if hexa else 'localizaciones'
    t_cache = 'cache_%s_resultados_%s' % (election, suffix)
    t_winner = 'cache_%s_winner_%s' % (election, suffix)
    query = template % {'cache': t_cache, 'winner': t_winner, 'key': key}
    print query
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    try:
        cur.execute(query)
    except psycopg2.Error, e:
        e.pgcode
    conn.commit()


def process_new_status(elec, hexa):
    '''process cache new status'''
    template = update_cache_set_new_status
    election = elec_arr[elec]
    if elec > 0:
        prev = elec_arr[elec-1]
        key = 'id_hexagono' if hexa else 'id_agrupado'
        suffix = 'hexagonos' if hexa else 'localizaciones'
        t_cache = 'cache_%s_resultados_%s' % (election, suffix)
        t_winner = 'cache_%s_winner_%s' % (election, suffix)
        t_wprev = 'cache_%s_winner_%s' % (prev, suffix)
        query = template % {'cache': t_cache, 'winner': t_winner,
                            'wprev': t_wprev, 'key': key}
        print query
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        try:
            cur.execute(query)
        except psycopg2.Error, e:
            e.pgcode
        conn.commit()


def run(args):
    '''process selected hexagon results'''
    process_winner_status(elec=args.elec, hexa=args.hexa)
    process_new_status(elec=args.elec, hexa=args.hexa)

if __name__ == '__main__':
    # Arguments handling
    parser = argparse.ArgumentParser()
    parser.add_argument("-e",
                        "--elec",
                        type=int,
                        default=0,
                        help="election to calculate results")
    parser.add_argument("-x",
                        "--hexa",
                        help="hexagons or polling stations",
                        action="store_true")
    args = parser.parse_args()
    run(args)
