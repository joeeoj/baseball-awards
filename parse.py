"""Script to parse CY, MVP, and ROY baseball reference award pages.

The award pages can't be downloaded with something like requests because the server fills in the tables over time.
The fastest way to get this info is to save them manually (literally Cmd/Ctrl + S) using your browser but if this
needed to be scaled up for many years, something like Selenium could be used.

example page to download: https://www.baseball-reference.com/awards/awards_2021.shtml
"""
import csv
from pathlib import Path, PosixPath
from typing import Generator

import bs4


INPUT_DIR = Path.cwd() / 'pages'
OUTPUT_DIR = Path.cwd() / 'data'
DATABANK_DIR = Path.cwd() / 'contrib'

BASE_TABLE_ID = '{league}_{award}_voting'
PLAYER_AWARDS = ['CYA', 'MVP', 'ROY']  # MOY seperate
LEAGUES = ['AL', 'NL']

COMMON_HEADER = ['year', 'award', 'league', 'bbref_id']
PLAYER_HEADER = COMMON_HEADER + ['name', 'team', 'points', 'votes_first', 'share_first', 'WAR', 'G', 'AB', 'R', 'H',
                                 'HR', 'RBI', 'SB', 'BB', 'AVG', 'OBP', 'SLG', 'OPS', 'W', 'L', 'ERA', 'WHIP', 'G_p',
                                 'GS', 'SV', 'IP', 'H_p', 'HR_p', 'BB_p', 'SO_p']
MANAGER_HEADER = COMMON_HEADER + ['name', 'team', 'points', 'votes_first', 'share_first', 'W', 'L', 'WL_pct', 'ties',
                                  'G', 'finish']


class Parser:
    def __init__(self, fname: PosixPath):
        self.fname = fname

        with open(fname) as f:
            page = f.read()

        self.soup = bs4.BeautifulSoup(page, 'html.parser')

        canonical = self.soup.select('link[rel*=canonical]')[0].get('href')
        self.year = Path(canonical).name.replace('.shtml', '').split('_')[-1]


    def _parse_bbref_id(self, href: str) -> str:
        """Parse bbref id from player/manager href"""
        return Path(href).name.replace('.shtml', '')


    def _get_table_rows(self, award: str) -> Generator[tuple[str, bs4.element.Tag], None, None]:
        """Return combined result set of both leagues for a given award"""
        for league in LEAGUES:
            table_id = BASE_TABLE_ID.format(league=league, award=award)
            rows = self.soup.find('table', id=table_id).find_all('tr')
            yield league, rows
  

    def _parse_row(self, row: bs4.element.Tag) -> list[str]:
        cells = row.find_all('td')
        if not cells:
            return []
        else:
            bbref_id = self._parse_bbref_id(cells[0].find('a').get('href'))
            data = [c.text.strip() if c.text.strip() != '' else None for c in cells]
            return [bbref_id] + data


    def _parse_table(self, award: str) -> list[str]:
        results = []
        for league, rows in self._get_table_rows(award):
            for row in rows:
                parsed = self._parse_row(row)
                if parsed:
                    results.append([self.year, award, league] + parsed)
        return results


    @property
    def players(self):
        players = []
        for award in PLAYER_AWARDS:
            players.extend(self._parse_table(award))
        return players


    @property
    def managers(self):
        return self._parse_table('MOY')


def write_csv(data: list[str], fout: PosixPath, header: list[str]) -> None:
    with open(fout, 'wt') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(header)
        csvwriter.writerows(data)


def main():
    for fname in INPUT_DIR.glob('*.shtml'):
        p = Parser(fname)
        write_csv(p.players, OUTPUT_DIR / f'player_awards_{p.year}.csv', PLAYER_HEADER)
        write_csv(p.managers, OUTPUT_DIR / f'manager_awards_{p.year}.csv', MANAGER_HEADER)


if __name__ == '__main__':
    main()
