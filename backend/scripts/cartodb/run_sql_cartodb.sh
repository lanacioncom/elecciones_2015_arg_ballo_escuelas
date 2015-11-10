#!/bin/sh
SCRIPTPATH=$( cd $(dirname $0) ; pwd -P )
# read configuration from env vars, args or default values
sql=$1
if [ $# -eq 1 ]
  then
    echo "Retrieve API keys and user from env vars"
    CARTODB_USER=${CARTODB_USER:-'cartodb'}
    API_KEY=${API_KEY:-'9999'}
else
    CARTODB_USER=$2
    API_KEY=$3
fi

query="q="
url="https://$CARTODB_USER.cartodb.com/api/v2/sql/?api_key=$API_KEY"
echo "Run $sql on cartodb"
curl $url -d $query$sql
