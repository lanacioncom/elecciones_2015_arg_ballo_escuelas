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
class BatchCompletionCallBack(object):
    completed = defaultdict(int)

    def __init__(self, dispatch_timestamp, batch_size, parallel):
        self.dispatch_timestamp = dispatch_timestamp
        self.batch_size = batch_size
        self.parallel = parallel

    def __call__(self, out):
        BatchCompletionCallBack.completed[self.parallel] += 1
        if BatchCompletionCallBack.completed[self.parallel] % 10 == 0:
            print("processed {} items"
                  .format(BatchCompletionCallBack.completed[self.parallel]))
        if self.parallel._original_iterator is not None:
            self.parallel.dispatch_next()
# MonkeyPatch BatchCompletionCallBack
joblib.parallel.BatchCompletionCallBack = BatchCompletionCallBack


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
    obj_list = client.documents.search(
        'title:%s' % (title),
        page=1,
        per_page=10)
    print obj_list
    if len(obj_list):
        print "%s not in DocumentCloud yet, upload" % (title)
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
    return None


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
    fpath = '%s/%s/%s' % (INPUT_PATH, 'pdf', row['key'])
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
