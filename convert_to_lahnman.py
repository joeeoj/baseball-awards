"""Convert raw baseball reference data to Lahnman data format for contribution to:

https://github.com/chadwickbureau/baseballdatabank/tree/master/contrib
"""
from collections import defaultdict
import csv
from itertools import chain
import json
from pathlib import Path, PosixPath


INPUT_DIR = Path.cwd() / 'data'
OUTPUT_DIR = Path.cwd() / 'contrib'
AWARD_NAMES = {'CYA': 'Cy Young', 'MVP': 'MVP', 'ROY': 'Rookie of the Year', 'MOY': 'BBWAA Manager of the Year'}
HEADER = ['awardID', 'yearID', 'lgID', 'playerID', 'pointsWon', 'pointsMax', 'votesFirst']

with open(INPUT_DIR / 'max_points.json') as f:
    MAX_POINTS = json.load(f)

with open(INPUT_DIR / 'bbref_to_lahnman.json') as f:
    MISMATCHES = json.load(f)


def str_to_int(s: str) -> int:
    """Try to convert string to integer otherwise return original input"""
    try:
        return int(s.replace('.0', ''))
    except ValueError:
        return s


def truncate_results(fname: PosixPath) -> list[dict]:
    """Truncate full csvs to Lahnman db fields"""
    with open(fname) as f:
        csvreader = csv.DictReader(f)
        data = [row for row in csvreader]

    results = []
    for row in data:
        bbref_id = row.get('bbref_id')
        year = row.get('year')
        league = row.get('league')
        award = row.get('award')
        max_points = MAX_POINTS[year][league][award]

        results.append({
            'awardID': AWARD_NAMES.get(award),
            'yearID': year,
            'lgID': league,
            'playerID': MISMATCHES.get(bbref_id, bbref_id),  # fall back to bbref if not a mismatch
            'pointsWon': str_to_int(row.get('points')),
            'pointsMax': max_points,
            'votesFirst': str_to_int(row.get('votes_first')),
        })
    return results


def write_dict_csv(data: list[str], fout: PosixPath) -> None:
    """Write both player and manager files (same header)"""
    with open(OUTPUT_DIR / fout, 'wt') as f:
        csvwriter = csv.DictWriter(f, fieldnames=HEADER)
        csvwriter.writeheader()
        csvwriter.writerows(data)


def sorter(data: list[dict]) -> list[dict]:
    """First sort by points, then the rest"""
    v = sorted(data, key=lambda d: d['pointsWon'], reverse=True)
    return sorted(v, key=lambda d: (d['yearID'], len(d['awardID']), d['lgID']))


def main():
    players = chain.from_iterable([truncate_results(fname) for fname in INPUT_DIR.glob('player*.csv')])
    players = sorter(list(players))
    write_dict_csv(players, 'AwardsSharePlayers.csv')

    managers = chain.from_iterable([truncate_results(fname) for fname in INPUT_DIR.glob('manager*.csv')])
    managers = sorter(list(managers))
    write_dict_csv(managers, 'AwardsShareManagers.csv')


if __name__ == '__main__':
    main()
