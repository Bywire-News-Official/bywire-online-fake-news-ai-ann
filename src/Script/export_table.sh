#!/bin/bash
# Declare an array of string with type
DB="bywire_trust"
OUTPUT="../Data/$1.json"
mongoexport -h 127.0.0.1:27017 -d $DB -c $1 --jsonArray -o $OUTPUT

