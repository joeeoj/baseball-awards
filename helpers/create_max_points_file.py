"""Construct max_points.json which contains the maximum points a candidate can win for a given award by year and league.

Structured by year -> league -> award

I had a convoluted way to calculate this but realized it's just total teams per league times points for first place.
The first place points per award seem static for now.
"""
import json
from pathlib import Path


DATA_DIR = Path.cwd().parent / 'data'

AWARDS = ['CYA', 'MVP', 'ROY', 'MOY']
BALLOTS_BY_YEAR = {
    2012: {'AL': 28, 'NL': 32},
    2013: {'AL': 30, 'NL': 30},
    2014: {'AL': 30, 'NL': 30},
    2015: {'AL': 30, 'NL': 30},
    2016: {'AL': 30, 'NL': 30},
    2017: {'AL': 30, 'NL': 30},
    2018: {'AL': 30, 'NL': 30},
    2019: {'AL': 30, 'NL': 30},
    2020: {'AL': 30, 'NL': 30},
    2021: {'AL': 30, 'NL': 30},
}
FIRST_PLACE_POINTS = {
    'CYA': 7,
    'MVP': 14,
    'ROY': 5,
    'MOY': 5,
}


if __name__ == '__main__':
    MAX_POINTS = {}
    for year, ballots in BALLOTS_BY_YEAR.items():
        MAX_POINTS[year] = {}

        for league, total_ballots in ballots.items():
            MAX_POINTS[year][league] = {}

            for award in AWARDS:
                MAX_POINTS[year][league][award] = total_ballots * FIRST_PLACE_POINTS[award]

    with open(DATA_DIR / 'max_points.json', 'wt') as f:
        json.dump(MAX_POINTS, f, indent=2)
