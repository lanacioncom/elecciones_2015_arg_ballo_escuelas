# coding: utf-8
import os

# DB CONNECTION
DB = os.environ.get('DATABASE_URL',
                    'postgresql://user:pass@localhost:5432/dbname')

# CARTODB API CREDENTIALS
CDB_USER = os.environ.get('CARTODB_USER', 'user')
CDB_KEY = os.environ.get('API_KEY', 'key')
