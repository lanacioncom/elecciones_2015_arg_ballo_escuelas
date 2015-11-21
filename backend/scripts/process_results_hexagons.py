# coding: utf-8
import argparse
import os
import psycopg2
from time import time
from settings import DATABASE_URL
from lqueries import insert_winner_hex_sql
from lqueries import insert_hex_results_sql
from lqueries import cache_insert_paso_results_hex_sql
from lqueries import cache_insert_pv_results_hex_sql
from lqueries import cache_insert_ballo_results_hex_sql

cache_elec_sw = {
    'e0': cache_insert_paso_results_hex_sql,
    'e1': cache_insert_pv_results_hex_sql,
    'e2': cache_insert_ballo_results_hex_sql
}

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


def process_results(elec):
    '''process'''
    print "calculate results for every hexagon and election"
    template = insert_hex_results_sql
    election = elec_arr[elec]
    dest = '%s_resultados_hexagonos' % (election)
    t_table = '%s_totales_localizaciones' % (election)
    r_table = '%s_resultados_localizaciones' % (election)
    query = template % {'totals': t_table, 'results': r_table, 'dest': dest}
    print query
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    try:
        cur.execute(query)
    except psycopg2.Error, e:
        e.pgcode
    conn.commit()


def process_cache_results(elec):
    '''calculate results for all hex levels'''
    print "calculate results for all hex levels"
    query = cache_elec_sw["e%d" % (elec)]
    print query
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    try:
        cur.execute(query)
    except psycopg2.Error, e:
        print e.pgerror
    # For testing purposes
    # print cur.fetchone()
    conn.commit()


def run(args):
    '''process selected hexagon results'''
    if args.winner:
        process_winner(elec=args.elec)
    elif args.cache:
        process_cache_results(elec=args.elec)
    else:
        process_results(elec=args.elec)

if __name__ == '__main__':
    # Arguments handling
    parser = argparse.ArgumentParser()
    parser.add_argument("-e",
                        "--elec",
                        type=int,
                        default=0,
                        help="election to calculate results")
    parser.add_argument("-c",
                        "--cache",
                        help="generate cache data",
                        action="store_true")
    parser.add_argument("-w",
                        "--winner",
                        help="generate winner data",
                        action="store_true")
    args = parser.parse_args()
    run(args)
