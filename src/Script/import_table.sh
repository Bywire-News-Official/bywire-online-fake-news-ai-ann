#!/bin/bash
# Declare an array of string with type
DB="bywire_trust"
INPUT="../Data/$1.json"
mongoimport -h 127.0.0.1:27017 -d $DB -c $1 --jsonArray $INPUT
