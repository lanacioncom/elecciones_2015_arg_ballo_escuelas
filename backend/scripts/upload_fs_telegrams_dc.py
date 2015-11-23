# coding: utf-8
import argparse
import os
from csvkit.py2 import CSVKitDictReader
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
N_CORES = 4


def upload_telegram(folder=None, client=None, row=None):
    '''Upload pdf from fs'''
    title = row['key'].replace(".pdf", "")
    fpath = '%s/%s/%s' % (INPUT_PATH, folder, row['key'])
    print fpath
    obj_list = client.documents.search(
        'title:%s' % (title),
        page=1,
        per_page=10)
    print obj_list
    if not len(obj_list):
        new_id = client.documents.upload(
            fpath,
            title=title,
            access='public',
            source='http://www.resultados.gob.ar/'
        )
        print new_id
        return new_id
    else:
        return None


def process_telegrams(fname=None):
    '''Download telegrams from gov site'''
    # Create output files folder if needed
    client = DocumentCloud(DOCUMENTCLOUD_USERNAME, DOCUMENTCLOUD_PASSWORD)
    # Create the project
    project, created = client.projects.get_or_create_by_title("2015 Elecciones Ballottage Telegramas")
    with open('%s/%s.csv' % (INPUT_PATH, fname), 'r') as f:
        reader = CSVKitDictReader(f)
        r = Parallel(n_jobs=N_CORES)(delayed(upload_telegram)(fname, client, row)
                                     for row in reader)

        print('finished processing {}.csv'.format(fname))
        r = filter(None, r)
        if len(r):
            print len(r)
            project.document_list = r
            # Save the changes to the project
            project.put()


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
