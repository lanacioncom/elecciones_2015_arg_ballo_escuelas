# coding: utf-8
import requests
import os
from csvkit.py2 import CSVKitDictReader, CSVKitDictWriter
import shutil
# Parallel execution libs
from joblib import Parallel, delayed
from collections import defaultdict
import joblib.parallel

BASE_URL = 'http://www.resultados.gob.ar/nacionaltelegr'


# PARALLEL EXECUTION SETTINGS
# Override joblib callback default callback behavior
class CallBack(object):
    completed = defaultdict(int)

    def __init__(self, index, parallel):
        self.index = index
        self.parallel = parallel

    def __call__(self, index):
        CallBack.completed[self.parallel] += 1
        if CallBack.completed[self.parallel] % 10 == 0:
            print("processed {} items"
                  .format(CallBack.completed[self.parallel]))
        if self.parallel._original_iterable:
            self.parallel.dispatch_next()
# MonkeyPatch Callback
joblib.parallel.CallBack = CallBack


# GLOBAL SETTINGS
cwd = os.path.dirname(__file__)
INPUT_PATH = os.path.join(cwd, '../data/telegrams')
INPUT_FILE = 'telegrams'
OUTPUT_FILE = 'telegrams_processed'
HEADER = ['id_agrupado', 'id_distrito', 'id_seccion',
          'id_circuito', 'key', 'fpath']
N_CORES = 7


def download_telegram(fext='pdf', row=None):
    '''Download an audio file'''
    result = row.copy()
    OUTPUT_PATH = '%s/%s' % (INPUT_PATH, fext)
    fpath = '%s/%s.%s' % (
        OUTPUT_PATH,
        row['key'],
        fext)
    result['fpath'] = fpath
    url = '%s/%s.%s' % (BASE_URL, row['key'], fext)
    if os.path.isfile(fpath):
        pass
    else:
        try:
            response = requests.get(url, stream=True)
            with open(fpath, 'wb') as of:
                shutil.copyfileobj(response.raw, of)
            del response
        except Exception:
            print('Error while downloading {}...skipping'
                  .format(url))
    return result


def process_telegrams(fext='pdf'):
    '''Download telegrams from gov site'''
    # Create output files folder if needed
    OUTPUT_PATH = '%s/%s' % (INPUT_PATH, fext)
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
    with open('%s/%s_%s.csv' %
              (INPUT_PATH, OUTPUT_FILE, fext), 'w') as fout:
        writer = CSVKitDictWriter(fout, fieldnames=HEADER)
        writer.writeheader()
        with open('%s/%s.csv' % (INPUT_PATH, INPUT_FILE), 'r') as f:
            reader = CSVKitDictReader(f)
            r = Parallel(n_jobs=N_CORES)(delayed(download_telegram)(fext, row)
                                         for row in reader)
            print('finished processing {}.csv'.format(INPUT_FILE))
            writer.writerows(r)


def run():
    # Download telegrams
    # process_telegrams(fext='pdf')
    process_telegrams(fext='html')

if __name__ == '__main__':
    run()
