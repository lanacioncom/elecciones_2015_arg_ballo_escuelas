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
OUTPUT_PATH = os.path.join(cwd, '../data/telegrams')
HEADER = ['document_id', 'document_title', 'project_id']
N_CORES = 4


def get_proj_docs_dc(client=None, proj=None):
    '''delete pdf from DocumentCloud'''
    result = []
    obj = client.projects.get(id=proj)
    print len(obj.document_ids)
    for doc in obj.document_ids:
        id = doc.split("-")[0]
        title = doc.split("-")[1]
        r = {'document_id': id, 'document_title': title, 'project_id': proj}
        print r
        result.append(r)
    return result


def process_telegrams(fname=None, proj=None):
    '''Download telegrams from gov site'''
    # Create output files folder if needed
    client = DocumentCloud(DOCUMENTCLOUD_USERNAME, DOCUMENTCLOUD_PASSWORD)
    with open('%s/%s.csv' %
              (OUTPUT_PATH, fname), 'w') as fout:
        writer = CSVKitDictWriter(fout, fieldnames=HEADER)
        writer.writeheader()
        r = get_proj_docs_dc(client, proj)
        writer.writerows(r)

        print('finished processing {}.csv'.format(fname))


def run(args):
    '''Let DC get the telegrams for us'''
    process_telegrams(args.file, args.project)

if __name__ == '__main__':
    # Arguments handling
    parser = argparse.ArgumentParser()
    parser.add_argument("-f",
                        "--file",
                        type=str,
                        required=True,
                        help="index file with telegram keys")
    parser.add_argument("-p",
                        "--project",
                        type=str,
                        required=True,
                        help="project id in DC")
    args = parser.parse_args()
    run(args)
