# coding: utf-8
import argparse
import os
from csvkit.py2 import CSVKitDictReader
from documentcloud import DocumentCloud
from documentcloud import DoesNotExistError
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
N_CORES = 4


def delete_telegram(client=None, row=None):
    '''delete pdf from DocumentCloud'''
    id = row['dc_id']
    try:
        obj = client.documents.get(id)
        print obj.title
        obj.delete()
    except DoesNotExistError, e:
        print e
    return None


def process_telegrams(fname=None):
    '''Download telegrams from gov site'''
    # Create output files folder if needed
    client = DocumentCloud(DOCUMENTCLOUD_USERNAME, DOCUMENTCLOUD_PASSWORD)
    with open('%s/%s.csv' % (INPUT_PATH, fname), 'r') as f:
        reader = CSVKitDictReader(f)
        r = Parallel(n_jobs=N_CORES)(delayed(delete_telegram)(client, row)
                                     for row in reader)

        print('finished processing {}.csv'.format(fname))


def run(args):
    '''Let DC get the telegrams for us'''
    process_telegrams(args.file)

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
