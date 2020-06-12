#!/usr/bin/env bash

cd "$(dirname $0)"

if [ ! -d venv ]
then  python -m venv venv
      pip install -r requirements.txt
fi

source venv/bin/activate
python crawler.py
