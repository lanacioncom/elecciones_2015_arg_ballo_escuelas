Backend information
===================

## Introduction

For the backend we have downloaded the official Windows election results app (PASO, first round & ballotage) provided by the government and extracted the underlying MS Access databases. Using _mdb-export_ from [mdbtools](https://github.com/brianb/mdbtools) we have converted the required tables into CSV files.

We also had the geolocated polling stations provided by the city electoral board in CSV format.

After obtaining all the source files in an appropiate format we have launch a transformation process that consists of roughly the following main steps:

1. Creating the postgres DB and schema.

2. Preprocessing the input datasets to facilitate the aggregation process.

3. Running the main transformation script (uses [_dataset_](https://dataset.readthedocs.org/en/latest/)) that aggregates the results by polling station.

4. Running the script that generates and calculates the hexagons for the required zoom levels.

5. Exporting the results to CSV files that would be then uploaded mannually to cartoDB.

We can then import the final results to _cartodb_ postgis DB. This is done mannually because it is a potentially destructive operation. Please make sure you understand the implications before proceeding.

* We have used postgres as the DB because our final destination was the cartodb postgis DB and also because of the magic behind [postgres window functions](http://www.postgresql.org/docs/9.4/static/functions-window.html) that we have used to create the margin of victory of a party over the next one in a given polling station directly on SQL.

## Usage info

### Requirements

* Have postgreSQL 9.x installed locally
* Python 2.7.\* && virtualenv && pip installed 

### Process

1. Create a virtualenv

        $ virtualenv .venv

2. Activate the created virtualenv

        $ source .venv/bin/activate

3. Install dependencies

        $ pip install -r requirements.txt

4. Create environment variables or change the default values 
    * _fabfile/settings.py_:
        * DATABASE_URL: Postgres DB that will store the transformation results
        * CARTODB API USER: CartoDB API account info
        * CARTODB API KEY: CartoDB API account info
    * _scripts/settings.py_:
        * DATABASE_URL: Postgres DB that will store the transformation results
        * DC_USER: Document Cloud API account info
        * DC_PASS: Document Cloud API account info

5. Launch the combined transformation process

        $ fab run

** Warning: Next steps are destructive so continue only if you are sure of what you are doing **

6. Run the fabric tasks that upsert the tables inside CartoDB 

        $ fab cartodb.import_common
        $ fab cartodb.import_shortcuts
        $ fab cartodb.import_hexagons
        $ fab cartodb.import_ballo_results
        $ fab cartodb.import_pv_results
        $ fab cartodb.import_paso_results
        $ fab cartodb.crowdsource
        $ fab cartodb.search
        $ fab cartodb.create_indexes

## Implementation notes

### Generating the precached hexagons

Due to performance problems calculating hexagon grids for Argentina's polling stations with a small hexagon that we thought was needed to allow for the user to explore the data with a proper granularity we had to take another approach and decided to precalculate the hexagon grids for our data and every zoom level that we were going to cover.

This process was quite CPU consuming specially on greater zoom levels were the number of hexagons to be calculated was in the order or billions.

We copied the required opensourced cartodb functions and extensions to a local postgis instance check [here](data/sql/create_cartodb_functions.sql) and included the generation process in our overall general fabric task.

### Tweaking dataset for CSV quote generation

We had to tweak _dataset_ CSVSerializer to allow imports to cartoDB without automatic type detection enabled. That way we could upload directly from the dataset freeze export without having to touch ids that were treated as numbers and not strings

        ```python
            # Hack for cartodb import
            writer = csv.writer(fh, quoting=csv.QUOTE_NONNUMERIC)
        ```

### DocumentCloud storage of official telegrams

This elections we had decided to scrape the telegrams provided in the official electoral website and upload them into DocumentCloud so that we could ensure a more permanent hosting of those documents.

We have used the DocumentCloud API extensively to import almost 100.000 documents to their servers. Because are work was being carried in python we have used the [python wrapper](http://python-documentcloud.readthedocs.org/en/latest/) and found it pretty straight forward to use.
