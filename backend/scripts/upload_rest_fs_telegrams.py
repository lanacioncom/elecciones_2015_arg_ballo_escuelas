# coding: utf-8
import argparse
import os
from csvkit.py2 import CSVKitDictReader, CSVKitDictWriter
from documentcloud import DocumentCloud
from time import time
from settings import DOCUMENTCLOUD_USERNAME, DOCUMENTCLOUD_PASSWORD

# Parallel execution libs
from joblib import Parallel, delayed
from collections import defaultdict
import joblib.parallel


# PARALLEL EXECUTION SETTINGS
# Override joblib callback default callback behavior
class CallBack(object):
    completed = defaultdict(int)

    def __init__(self, index, parallel):
        self.index = index
        self.parallel = parallel

    def __call__(self, index):
        CallBack.completed[self.parallel] += 1
        if CallBack.completed[self.parallel] % 100 == 0:
            print("processed {} items"
                  .format(CallBack.completed[self.parallel]))
        if self.parallel._original_iterable:
            self.parallel.dispatch_next()
# MonkeyPatch Callback
joblib.parallel.CallBack = CallBack


# GLOBAL SETTINGS
cwd = os.path.dirname(__file__)
INPUT_PATH = os.path.join(cwd, '../data/telegrams')
UPLOADED_FILE = 'uploaded'
N_CORES = 6
PROJECT_ID = '23498'
HEADER = ['document_id', 'document_title', 'project_id']


def load_prev_uploaded():
    '''Already uploaded telegrams to DocumentCloud'''
    s = None
    # Create output files folder if needed
    with open('%s/%s.csv' % (INPUT_PATH, UPLOADED_FILE), 'r') as f:
        reader = CSVKitDictReader(f)
        s = set([r['document_title'] for r in reader])
    return s


def upload_telegram(folder=None, client=None, cache_set=None, row=None):
    '''Upload pdf from fs'''
    result = {}
    title = row['key'].replace(".pdf", "")
    result['document_title'] = title
    result['project_id'] = PROJECT_ID
    fpath = '%s/%s/%s' % (INPUT_PATH, folder, row['key'])
    if title in cache_set:
        print "%s already uploaded" % (title)
    else:
        print "%s not in DocumentCloud yet, upload" % (title)
        dc_obj = client.documents.upload(
            fpath,
            title=title,
            project=PROJECT_ID,
            access='public',
            source='http://www.resultados.gob.ar/'
        )
        dc_id = dc_obj.id.split('-')[0]
        print dc_id
        result['document_id'] = dc_id
        return result


def process_telegrams(cache_set, fname=None):
    '''Download telegrams from gov site'''
    # Create output files folder if needed
    client = DocumentCloud(DOCUMENTCLOUD_USERNAME, DOCUMENTCLOUD_PASSWORD)

    with open('%s/uploaded_%s.csv' % (INPUT_PATH, fname), 'w') as fout:
        writer = CSVKitDictWriter(fout, fieldnames=HEADER)
        writer.writeheader()
        # Create the project
        with open('%s/%s.csv' % (INPUT_PATH, fname), 'r') as f:
            reader = CSVKitDictReader(f)
            r = Parallel(n_jobs=N_CORES)(delayed(upload_telegram)(
                    fname,
                    client,
                    cache_set,
                    row)
                    for row in reader)

            print('finished processing {}.csv'.format(fname))
        print "Longitud del dataset de resultados sin filtrar: %s" % (len(r))
        r = filter(None, r)
        print "Longitud del dataset de resultados filtrados: %s" % (len(r))
        if len(r):
            writer.writerows(r)


def test_dc_upload(cache_set, row):
    '''just for testing purposes prio to bulk upload'''
    result = {}
    title = row['key'].replace(".pdf", "")
    result['document_title'] = title
    result['project_id'] = PROJECT_ID
    client = DocumentCloud(DOCUMENTCLOUD_USERNAME, DOCUMENTCLOUD_PASSWORD)
    fpath = '%s/%s/%s' % (INPUT_PATH, 'pdf1', row['key'])
    if title in cache_set:
        print "%s already uploaded" % (title)
        # return None
    else:
        print "%s not in DocumentCloud yet, upload" % (title)
        dc_obj = client.documents.upload(
                fpath,
                title=title,
                project=PROJECT_ID,
                access='public',
                source='http://www.resultados.gob.ar/'
        )
        dc_id = dc_obj.id.split('-')[0]
        import pdb; pdb.set_trace()
        print "DC document_id: %s" % (dc_id)
        result['document_id'] = dc_id
        return result
    return None


def run(args):
    '''Let DC get the telegrams for us'''
    cache_set = load_prev_uploaded()
    # test_dc_upload(cache_set, {u'key': u'24_003_0024_240030024_0436.pdf'})
    process_telegrams(cache_set, args.file)

if __name__ == '__main__':
    # Arguments handling
    parser = argparse.ArgumentParser()
    parser.add_argument("-f",
                        "--file",
                        type=str,
                        required=True,
                        help="index file with telegram keys")
    args = parser.parse_args()
    run(args)
