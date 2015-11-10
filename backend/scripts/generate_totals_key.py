#!/usr/bin/env python
# coding: utf-8
import os
from csvkit.py2 import CSVKitDictReader, CSVKitDictWriter
from time import time
from settings import INPUT_PASO_PATH, OUTPUT_PASO_PATH
from settings import INPUT_PV_PATH, OUTPUT_PV_PATH
from settings import INPUT_BALLO_PATH, OUTPUT_BALLO_PATH

HEADER = [
    'key_circ',
    'key_wo_circ',
    'id_distrito',
    'id_seccion',
    'id_circuito',
    'id_mesa',
    'electores',
    'votantes',
    'validos',
    'positivos',
    'blancos',
    'nulos'
]

# INPUT PATH, OUTPUT PATH, AND QUOTES FOR EACH ELECTION RESULTS
ELEC_CONFIG = {
    'paso': [INPUT_PASO_PATH, OUTPUT_PASO_PATH, '"'],
    'pv': [INPUT_PV_PATH, OUTPUT_PV_PATH, "'"],
    'ballo': [INPUT_BALLO_PATH, OUTPUT_BALLO_PATH, "'"]
}


def format_circuit(c):
    '''format circuit to 5 chars'''
    result = None
    c = c.upper().strip()
    if len(c) == 4:
        result = '0'+c
    else:
        result = c
    return result


def generate_key(row, circ=True):
    '''generates a key to join with the elections results data'''
    result = None
    result = row['id_distrito']
    result += "_"+row['id_seccion']
    if circ:
        result += "_"+row['id_circuito']
    result += "_"+row['id_mesa']
    return result


def clean_row(row):
    '''transforms each row to desired output format'''
    try:
        # rename and transform fields
        row['id_distrito'] = row['mes_proCodigoProvincia']
        row['id_seccion'] = row['mes_depCodigoDepartamento']
        row['id_circuito'] = format_circuit(row['mesCodigoCircuito'])
        row['id_mesa'] = row['mesCodigoMesa']
        # rename results
        row['electores'] = row['mesElectores']
        row['votantes'] = row['mesTotalVotantes']
        row['validos'] = row['mesVotosValidos']
        row['positivos'] = row['mesVotosPositivos']
        row['blancos'] = row['mesVotosEnBlanco']
        row['nulos'] = row['mesVotosNulos']

        # create keys
        row['key_circ'] = generate_key(row, circ=True)
        row['key_wo_circ'] = generate_key(row, circ=False)
        return row
    except ValueError as e:
        print "could not convert to int. Reason %s" % (e)
        raise


def create_key_file(fname, elec='paso'):
    '''generate key to assign polling station'''
    input_path = ELEC_CONFIG[elec][0]
    output_path = ELEC_CONFIG[elec][1]
    quotes = ELEC_CONFIG[elec][2]
    # Create folders
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Open output file in write mode
    with open('%s/%s_key.csv'
              % (output_path, fname), 'w') as fout:
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
                  % (input_path, fname), 'r') as f:
            reader = CSVKitDictReader(f, quotechar=quotes)
            count = 0
            for row in reader:
                count += 1
                if (count % 10000 == 0):
                    print('processed %s polling tables' % (count))
                r = clean_row(row)
                results.writerow(r)


def _main():
    '''transform paso, pv and ballo input election totals files'''
    start_time = time()
    print "create paso polling station keys to facilitate joins"
    create_key_file('mesaspresidente', elec='paso')
    print "create pv polling station keys to facilitate joins"
    create_key_file('mesaspresidente', elec='pv')
    print "create ballo polling station keys to facilitate joins"
    create_key_file('mesaspresidente', elec='ballo')
    print "polling table key creation: %s seconds" % (time() - start_time)


if __name__ == "__main__":
    _main()
