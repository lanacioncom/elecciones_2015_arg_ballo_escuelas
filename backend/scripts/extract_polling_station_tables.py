#!/usr/bin/env python
# coding: utf-8
import os
import re
from time import time
from csvkit.py2 import CSVKitDictReader, CSVKitDictWriter
from settings import INPUT_COMMON_PATH, OUTPUT_COMMON_PATH

HEADER = [
    'id_establecimiento',
    'key_sie',
    'key_circ',
    'key_wo_circ',
    'id_distrito',
    'id_seccion',
    'id_circuito',
    'id_mesa',
    'key_telegrama'
]


def generate_key_telegrama(row=None):
    '''generates a key to access the telegram on the official website
    http://www.resultados.gob.ar/nacionaltelegr/05/003/0017/050030017_1032.htm
    http://www.resultados.gob.ar/nacionaltelegr/02/003/0018A/020030018A0158.htm
    http://www.resultados.gob.ar/nacionaltelegr/21/002/0365A/210020365A0138.htm
    http://www.resultados.gob.ar/nacionaltelegr/23/005/0060B/230050060B1736.htm
    http://www.resultados.gob.ar/nacionaltelegr/21/002/0365/210020365_0130.htm
    http://www.resultados.gob.ar/nacionaltelegr/01/001/0001/010010001_0001.htm
    05/003/0017/050030017_1032
    the orig id_circuito come on two forms 00001 or 0001A
    and we need 0001 (0001_) and 0001A
    '''
    circ_patt = re.compile("^\d{5}$")
    result = None

    if circ_patt.match(row['id_circuito']):
        circ = row['id_circuito'][1:]
    else:
        circ = row['id_circuito']
    result = row['id_distrito']+"/"+row['id_seccion']+"/"+circ+"/"
    result += row['id_distrito']
    result += row['id_seccion']
    result += circ
    if len(circ) == 4:
        result += '_'
    result += row['id_mesa']
    return result


def generate_key(row=None, circ=True):
    '''generates a key to join with the elections results data'''
    result = None
    result = row['id_distrito']
    result += "_"+row['id_seccion']
    if circ:
        result += "_"+row['id_circuito']
    result += "_"+row['id_mesa']
    return result


def extract_range(row=None):
    '''extracts a list of polling tables for a given range'''
    try:
        md = int(row['mesa_desde'])
        mh = int(row['mesa_hasta'])
        # If there is only one return it as a list
        if md == mh:
            row['id_establecimiento'] = row['id_establecimiento']
            row['id_mesa'] = "{0:04d}".format(int(row['mesa_desde']))
            row['key_circ'] = generate_key(row, circ=True)
            row['key_wo_circ'] = generate_key(row, circ=False)
            row['key_telegrama'] = generate_key_telegrama(row)
            return [row]

        # If there are more than one
        r = []
        for i in range(md, mh+1):
            rc = row.copy()
            rc['id_establecimiento'] = rc['id_establecimiento']
            rc['id_mesa'] = "{0:04d}".format(i)
            rc['key_circ'] = generate_key(rc, circ=True)
            rc['key_wo_circ'] = generate_key(rc, circ=False)
            rc['key_telegrama'] = generate_key_telegrama(rc)
            r.append(rc)
        return r
    except ValueError, e:
        print "could not convert to int. Reason %s" % (e)
        raise


def _main():
    '''extract individual tables from range'''
    start_time = time()
    # Create folders
    if not os.path.exists(OUTPUT_COMMON_PATH):
        os.makedirs(OUTPUT_COMMON_PATH)

    # Open output file in write mode
    with open('%s/%s_mesas.csv'
              % (OUTPUT_COMMON_PATH, 'establecimientos'), 'w') as fout:
        results = CSVKitDictWriter(
            fout,
            encoding='utf-8',
            # Ignore keys not in fieldnames
            extrasaction='ignore',
            fieldnames=HEADER)
        # Write header
        results.writeheader()

        # Open input file in read mode
        with open('%s/%s.csv'
                  % (INPUT_COMMON_PATH, 'establecimientos'), 'r') as f:
            reader = CSVKitDictReader(f)
            count = 0
            for row in reader:
                count += 1
                if (count % 1000 == 0):
                    print('processed %s polling stations' % (count))
                l = extract_range(row)
                results.writerows(l)
    print "extract individual tables: %s seconds" % (time() - start_time)


if __name__ == "__main__":
    _main()
