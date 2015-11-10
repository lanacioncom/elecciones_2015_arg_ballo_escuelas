#!/bin/sh
SCRIPTPATH=$( cd $(dirname $0) ; pwd -P )
CSV_PATH=$SCRIPTPATH'/../../data/cartodb'
# read configuration from env vars, args or default values
CSV_FILE=$1
if [ $# -eq 1 ]
  then
    echo "Retrieve API keys and user from env vars"
    CARTODB_USER=${CARTODB_USER:-'cartodb'}
    API_KEY=${API_KEY:-'9999'}
else
    CARTODB_USER=$2
    API_KEY=$3
fi
echo "import $CSV_FILE into cartodb (set privacy and do not parse quoted columns)"
curl -F file=@$CSV_FILE "https://$CARTODB_USER.cartodb.com/api/v1/imports/?api_key=$API_KEY&privacy=link&quoted_fields_guessing=false"