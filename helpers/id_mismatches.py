import csv
import json
from pathlib import Path


DATA_DIR = Path.cwd().parent / 'data'


MISMATCHES = {}
with open(DATA_DIR / 'People.csv') as f:
    csvreader = csv.DictReader(f)
    for row in csvreader:
        lahnman_id, bbref_id = row.get('playerID'), row.get('bbrefID')

        if bbref_id != '' and bbref_id != lahnman_id:
            MISMATCHES[bbref_id] = lahnman_id

with open(DATA_DIR / 'bbref_to_lahnman.json', 'wt') as f:
    json.dump(MISMATCHES, f, indent=2)
