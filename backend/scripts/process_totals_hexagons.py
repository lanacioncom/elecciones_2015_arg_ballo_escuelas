# coding: utf-8
import argparse
import os
import psycopg2
from time import time
from settings import DATABASE_URL
from lqueries import insert_hex_totales_sql
from lqueries import cache_insert_hex_totales_sql

elec_arr = ['paso', 'pv', 'ballo']


def process_totals_cache():
    '''process'''
    print "calculate totals for every hexagon"
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    try:
        cur.execute(cache_insert_hex_totales_sql)
    except psycopg2.Error, e:
        e.pgcode
    conn.commit()


def process_totals(elec):
    '''process'''
    print "calculate totals for every hexagon and election"
    template = insert_hex_totales_sql
    election = elec_arr[elec]
    dest = '%s_totales_hexagonos' % (election)
    t_table = '%s_totales_localizaciones' % (election)
    query = template % {'totals': t_table, 'dest': dest}
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
    if args.cache:
        process_totals_cache()
    else:
        process_totals(elec=args.elec)

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
    args = parser.parse_args()
    run(args)
