#!/usr/bin/env bash
python3 -m venv atms_env
source atms_env/bin/activate
pip3 install -r requirements.txt
bash download_atms_info.sh
csv-to-sqlite -f atms.csv -t full -o atms.db
python3 setup_db.py
rm atms.csv
