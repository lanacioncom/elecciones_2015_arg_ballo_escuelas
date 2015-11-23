# coding: utf-8
import argparse
import os
from documentcloud import DocumentCloud
from time import time
from settings import DOCUMENTCLOUD_USERNAME, DOCUMENTCLOUD_PASSWORD
# LOCAL PATHS
cwd = os.path.dirname(__file__)
INPUT_PATH = os.path.join(cwd, '../data/telegrams/pdf1')


def run():
    '''upload telegram pdfs to DocumentCloud'''
    # Connect to documentcloud
    client = DocumentCloud(DOCUMENTCLOUD_USERNAME, DOCUMENTCLOUD_PASSWORD)
    # Create the project
    project, created = client.projects.get_or_create_by_title("2015 Elecciones Ballottage Telegramas")
    # Upload all the pdfs
    obj_list = client.documents.upload_directory(
        INPUT_PATH,
        access='public',
        source='http://www.resultados.gob.ar/'
    )
    print "done!!"
    # Add the newly created documents to the project
    project.document_list = obj_list
    # Save the changes to the project
    project.put()

if __name__ == "__main__":
    run()
