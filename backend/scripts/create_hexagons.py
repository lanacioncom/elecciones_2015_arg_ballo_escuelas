# coding: utf-8
import argparse
import os
import psycopg2
from time import time
from settings import DATABASE_URL
from lqueries import insert_hex_sql
from lqueries import insert_antartida_hex_sql
from lqueries import insert_hex_lzoom_sql


def run(args):
    '''generate hex data'''
    zoom = args.zoom
    size = args.size
    if args.low:
        query = insert_hex_lzoom_sql
        zold = zoom - 1
        data = {'z': zoom, 'zold': zold, 'size': size}
    elif args.antar:
        query = insert_antartida_hex_sql
        data = {'z': zoom, 'size': size}
    else:
        query = insert_hex_sql
        data = {'z': zoom, 'size': size}
    print "calculate hex for zoom: %s && hex multiplier: %s" % (zoom, size)
    conn = psycopg2.connect(DATABASE_URL)
    print query
    cur = conn.cursor()
    try:
        cur.execute(query, data)
    except psycopg2.Error, e:
        e.pgcode
    conn.commit()

if __name__ == '__main__':
    # Arguments handling
    parser = argparse.ArgumentParser()
    parser.add_argument("-z",
                        "--zoom",
                        type=int,
                        default=4,
                        help="zoom level for the hexagon grid")
    parser.add_argument("-s",
                        "--size",
                        type=float,
                        default=30,
                        help="multiplier for hexagon size")
    parser.add_argument("-a",
                        "--antar",
                        help="generate antartida hex data",
                        action="store_true")
    parser.add_argument("-l",
                        "--low",
                        help="low level hex generation",
                        action="store_true")
    args = parser.parse_args()
    run(args)
