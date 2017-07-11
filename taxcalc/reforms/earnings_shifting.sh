#!/bin/bash
# earnings_shifting.sh calls earnings_shifting.py and earnings_shifting.awk
# USAGE: ./earnings_shifting.sh

RUNS="STD"
#RUNS="TPC"

function es_run {
    python earnings_shifting.py $1 $2 $3 $4 $5 | awk -f earnings_shifting.awk
}

echo "STARTING : `date`"

HEADER="YEAR  WAGE_AMT   MIN_EARN  MIN_SAVE  SPROB :  NS(#m)    ES(\$b)  TAXDIFF(\$b)"
echo "${HEADER}"

# baseline results with no-earnings-shifting
es_run 2017 0.0 0.0 0.0 0.0

if [ "$RUNS" == "TPC" ]; then
    es_run 2017  0e3 1e5 0.0 0.5
    es_run 2017  1e3 1e5 0.0 0.5
    es_run 2017  2e3 1e5 0.0 0.5
    es_run 2017  3e3 1e5 0.0 0.5
    es_run 2017  4e3 1e5 0.0 0.5
    es_run 2017  5e3 1e5 0.0 0.5
    es_run 2017  6e3 1e5 0.0 0.5
    es_run 2017  7e3 1e5 0.0 0.5
    es_run 2017  8e3 1e5 0.0 0.5
    es_run 2017  9e3 1e5 0.0 0.5
    es_run 2017 10e3 1e5 0.0 0.5
    es_run 2017 15e3 1e5 0.0 0.5
    es_run 2017 20e3 1e5 0.0 0.5
    es_run 2017 25e3 1e5 0.0 0.5
    es_run 2017 30e3 1e5 0.0 0.5
    es_run 2017 35e3 1e5 0.0 0.5
    es_run 2017 40e3 1e5 0.0 0.5
fi

if [ "$RUNS" == "STD" ]; then
    es_run 2017 0.0 1e5 0.0 0.5
    es_run 2017 0.0 2e5 1e4 1.0
    es_run 2017 0.0 3e5 1e4 1.0
    es_run 2017 0.0 4e5 1e4 1.0
    es_run 2017 0.0 2e5 2e4 1.0
    es_run 2017 0.0 3e5 2e4 1.0
    es_run 2017 0.0 4e5 2e4 1.0
    es_run 2017 0.0 2e5 3e4 1.0
    es_run 2017 0.0 3e5 3e4 1.0
    es_run 2017 0.0 4e5 3e4 1.0
    es_run 2017 0.0 5e5 3e4 1.0
    es_run 2017 0.0 5e5 4e4 1.0
    es_run 2017 0.0 5e5 5e4 1.0
fi

echo "FINISHED : `date`"
exit 0
