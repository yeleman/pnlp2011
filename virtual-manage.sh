#!/bin/bash

DIR="$( cd "$( dirname "$0" )" && pwd )"
cd $DIR
source ../envs/pnlp/bin/activate
exec ./manage.py $@
