# coding: utf-8
import argparse
import os
import psycopg2
from time import time
from settings import DATABASE_URL
from lqueries import insert_hex_sql


def run(zoom, size):
    '''testing'''
    print "calculate hex for zoom: %s && hex multiplier: %s" % (zoom, size)
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    data = {'z': zoom, 'size': size}
    try:
        cur.execute(insert_hex_sql, data)
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
    args = parser.parse_args()
    run(zoom=args.zoom, size=args.size)
