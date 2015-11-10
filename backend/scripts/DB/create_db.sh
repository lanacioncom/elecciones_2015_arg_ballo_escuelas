#!/bin/bash
SCRIPTPATH=$( cd $(dirname $0) ; pwd -P )
# read configuration from env vars or default values
DATABASE_NAME=$1
echo "Creating $DATABASE_NAME"
dropdb --if-exists $DATABASE_NAME && createdb $DATABASE_NAME

