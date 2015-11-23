#!/usr/bin/env python
# coding: utf-8
import os
from csvkit.py2 import CSVKitDictReader, CSVKitDictWriter
from time import time
# Results simulation
import random
import copy
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
    'id_partido',
    'votos'
]

# INPUT AND OUTPUT PATH FOR EACH ELECTION RESULTS
ELEC_CONFIG = {
    'paso': [INPUT_PASO_PATH, OUTPUT_PASO_PATH],
    'pv': [INPUT_PV_PATH, OUTPUT_PV_PATH],
    'ballo': [INPUT_BALLO_PATH, OUTPUT_BALLO_PATH]
}

# #################SIMULATION FUNCTIONALITY ######################


def generate_sim_rows(row):
    '''rename columns and generate keys'''
    rows = [row, copy.copy(row)]
    parties = ['0131', '0135']
    try:
        pos = int(row['mesVotosPositivos'])
        rand_votes = assign_random_perc(pos)
    except ValueError, e:
        print "could not convert to int. Reason %s" % (e)
        raise

    for i, r in enumerate(rows):
        try:
            # rename and transform fields
            r['id_distrito'] = r['mes_proCodigoProvincia']
            r['id_seccion'] = r['mes_depCodigoDepartamento']
            r['id_circuito'] = format_circuit(row['mesCodigoCircuito'])
            r['id_mesa'] = row['mesCodigoMesa']
            # create keys
            # Start with FPV
            r['id_partido'] = parties[i]
            if not i:
                r['votos'] = rand_votes
            else:
                r['votos'] = pos - rand_votes
            r['key_circ'] = generate_key(row, circ=True)
            r['key_wo_circ'] = generate_key(row, circ=False)
        except ValueError as e:
            print "could not convert to int. Reason %s" % (e)
            raise
    return rows


def assign_random_perc(value=None):
    '''assign random percentage of votes, skip if 0'''
    result = None
    if value:
        result = int(random.random() * value)
    else:
        result = 0
    return result


# ##################END SIMULATION FUNCTIONALITY ###############


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
    '''extracts a list of polling tables for a given range'''
    try:
        # rename and transform fields
        row['id_distrito'] = row['vot_proCodigoProvincia']
        row['id_seccion'] = row['vot_depCodigoDepartamento']
        row['id_circuito'] = format_circuit(row['vot_mesCodigoCircuito'])
        row['id_mesa'] = row['vot_mesCodigoMesa']
        # rename results
        row['id_partido'] = row['vot_parCodigo']
        row['votos'] = row['votVotosPartido']
        # create keys
        row['key_circ'] = generate_key(row, circ=True)
        row['key_wo_circ'] = generate_key(row, circ=False)
        return row
    except ValueError as e:
        print "could not convert to int. Reason %s" % (e)
        raise


def create_key_file(fname, elec='paso', sim=False):
    '''generate key to assign polling station'''
    input_path = ELEC_CONFIG[elec][0]
    output_path = ELEC_CONFIG[elec][1]
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
        fname = 'mesaspresidente' if sim else fname
        with open('%s/%s.csv'
                  % (input_path, fname), 'r') as f:
            reader = CSVKitDictReader(f, quotechar="'")
            count = 0
            for row in reader:
                count += 1
                if (count % 50000 == 0):
                    print('processed %s polling tables' % (count))
                if sim:
                    rows = generate_sim_rows(row)
                    for r in rows:
                        results.writerow(r)
                else:
                    r = clean_row(row)
                    results.writerow(r)


def _main():
    '''transform paso, pv and ballo input election results files'''
    start_time = time()
    print "create paso polling station keys to facilitate joins"
    create_key_file('mesascandidaturapresidente', elec='paso')
    print "create pv polling station keys to facilitate joins"
    create_key_file('mesascandidaturapresidente', elec='pv')
    print "create ballo polling station keys to facilitate joins"
    create_key_file('mesascandidaturapresidente', elec='ballo')
    # create_key_file('mesascandidaturapresidente', elec='ballo', sim=True)
    print "polling table key creation: %s seconds" % (time() - start_time)


if __name__ == "__main__":
    _main()
