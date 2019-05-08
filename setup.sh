#!/usr/bin/env bash
python3 -m venv atms_env
source atms_env/bin/activate
pip3 install -r requirements.txt
bash download_atms_info.sh
csv-to-sqlite -f cajeros-automaticos.csv -t full -o cajeros-automaticos.db
python3 setup_db.py
