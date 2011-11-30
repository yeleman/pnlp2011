#!/bin/bash

#DEST="pnlp@yeleman.com,moussacoulibaly@sante.gov.ml"

DEST="reg@yeleman.com"

NOW=`date +%c`
export BALANCE_STR=`/home/pnlp/src/nosms/ussd.sh "*101#"`

BALANCE=`python -c "import os
import re
str_ = os.environ['BALANCE_STR'].strip().split(\"\n\")[-1]
try:
    print(re.search('Votre solde est de ([0-9]+) FCFA', str_).groups()[0])
except:
    print('?')"`

TITLE=`echo "[PNLP-SIM] Solde au $NOW: $BALANCE F CFA"`

echo $BALANCE_STR | mail -s "$TITLE" "$DEST"

export BALANCE_STR=
